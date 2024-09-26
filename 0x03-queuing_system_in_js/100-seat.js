import express from "express";
import { createClient } from 'redis';
import { promisify } from 'util';
import kue from "kue";


const client = createClient()

const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

client.on('error', err => {
  console.log(`Redis client not connected to the server: ${err}`)
});
client.on('connect', async () => {
  await setAsync('available_seats', 50)
});

const reserveSeat = async function (number) {
  await setAsync('available_seats', number)
}

const getCurrentAvailableSeats = async function () {
  const reply = await getAsync('available_seats')
  return Number(reply)
}

let reservationEnabled = true;
const queue = kue.createQueue();

const app = express();
app.listen(1245);

app.get('/available_seats', async (req, res) => {
  const CurrentAvailableSeats = await getCurrentAvailableSeats();
  res.send({ "numberOfAvailableSeats": CurrentAvailableSeats });
})

app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    res.send({ "status": "Reservation are blocked" });
  } else {
    const Job = queue.create('reserve_seat').save(err => {
      if (!err) res.send({ "status": "Reservation in process" });
      else res.send({ "status": "Reservation failed" });
    });

    Job.on('complete', () => {
      console.log(`Seat reservation job ${Job.id} completed`);
    }).on('failed', (err) => {
      console.log(`Seat reservation job ${Job.id} failed: ${err}`);
    });
  }
})

app.get('/process', async (req, res) => {
  queue.process('reserve_seat', async (job, done) => {
    const newCurrentAvailableSeats = (await getCurrentAvailableSeats() - 1);
    if (newCurrentAvailableSeats === 0) {
      reservationEnabled = false;
    }
    if (newCurrentAvailableSeats >= 0) {
      reserveSeat(newCurrentAvailableSeats);
      done();
    } else {
      done(new Error('Not enough seats available'));
    }
  })
  res.send({ "status": "Queue processing" });
})