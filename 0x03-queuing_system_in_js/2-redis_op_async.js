import { promisify } from 'util';
import redis from 'redis';
const createClient = redis.createClient

const client = createClient()
client
  .on('error', err => {
    console.log(`Redis client not connected to the server: ${err}`)
  })
  .on('connect', () => {
    console.log('Redis client connected to the server')
  })

const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

const setNewSchool = async function (schoolName, value) {
  const rep = await setAsync(schoolName, value);
  redis.print(`Reply: ${rep}`);
};

const displaySchoolValue = async function (schoolName) {
  const reply = await getAsync(schoolName);
  console.log(reply);
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');