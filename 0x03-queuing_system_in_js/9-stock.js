import express from "express";
import { createClient } from 'redis';
import { promisify } from 'util';

const listProducts = [
  {
    "itemId": 1,
    "itemName": "Suitcase 250",
    "price": 50,
    "initialAvailableQuantity": 4
  },
  {
    "itemId": 2,
    "itemName": "Suitcase 450",
    "price": 100,
    "initialAvailableQuantity": 10
  },
  {
    "itemId": 3,
    "itemName": "Suitcase 650",
    "price": 350,
    "initialAvailableQuantity": 2
  },
  {
    "itemId": 4,
    "itemName": "Suitcase 1050",
    "price": 550,
    "initialAvailableQuantity": 5
  }
];

const getItemById = (id) => {
  return listProducts.find(item => item.itemId.toString() === id);
}

const client = createClient()
client.on('error', err => {
  console.log(`Redis client not connected to the server: ${err}`)
})

const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

const reserveStockById = async function (itemId, stock) {
  await setAsync(itemId, stock);
}


const getCurrentReservedStockById = async function (itemId) {
  const reply = await getAsync(itemId)
  if (reply) {
    return reply
  } else {
    return 0
  }
}

const app = express();
app.listen(1245);

app.get('/list_products', (req, res) => {
  res.send(listProducts);
})

app.get('/list_products/:itemId', async (req, res) => {
  const item = getItemById(req.params.itemId);
  if (!item) {
    res.status(404).send({ "status": "Product not found" });
  } else {
    const CurrentReserved = await getCurrentReservedStockById(req.params.itemId);
    const itemWithReserved = {
      ...item,
      "currentQuantity": (item.initialAvailableQuantity - CurrentReserved)
    };
    res.send(itemWithReserved);
  }
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const item = getItemById(req.params.itemId);
  if (!item) {
    res.status(404).send({ "status": "Product not found" });
  } else {
    const CurrentReserved = await getCurrentReservedStockById(req.params.itemId);
    if (CurrentReserved >= item.initialAvailableQuantity) {
      res.status(400).send({ "status": "Not enough stock available", "itemId": item.itemId });
    } else {
      reserveStockById(item.itemId, (Number(CurrentReserved) + 1));
      res.send({ "status": "Reservation confirmed", "itemId": item.itemId });
    }
  }
});