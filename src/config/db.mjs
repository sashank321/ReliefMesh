import { MongoClient } from "mongodb";
import dotenv from "dotenv";

dotenv.config();

const MONGODB_URI = process.env.MONGODB_URI || "mongodb://127.0.0.1:27018/reliefmesh?replicaSet=rs0&directConnection=true";
const DB_NAME = process.env.DB_NAME || "reliefmesh";

let client = null;
let db = null;

export async function connectToDatabase() {
  if (db) return { client, db };

  try {
    client = new MongoClient(MONGODB_URI, {
      maxPoolSize: 50,
      minPoolSize: 10,
      serverSelectionTimeoutMS: 5000,
    });
    await client.connect();
    db = client.db(DB_NAME);
    console.log(`[MongoDB Core] Successfully connected to MongoDB Replica Set: ${MONGODB_URI}`);
    return { client, db };
  } catch (error) {
    console.error(`[MongoDB Core] Connection failed to ${MONGODB_URI}:`, error.message);
    throw error;
  }
}

export function getDb() {
  if (!db) {
    throw new Error("Database not connected. Call connectToDatabase() first.");
  }
  return db;
}

export function getClient() {
  if (!client) {
    throw new Error("Client not connected. Call connectToDatabase() first.");
  }
  return client;
}

export async function closeDatabase() {
  if (client) {
    await client.close();
    client = null;
    db = null;
    console.log("[MongoDB Core] Connection pool closed.");
  }
}
