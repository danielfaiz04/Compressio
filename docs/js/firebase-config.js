// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAgb2EzmCQ5kHE9TxAAnk7m4FSGbsDsGFE",
  authDomain: "compressio-78a31.firebaseapp.com",
  databaseURL: "https://compressio-78a31-default-rtdb.firebaseio.com",
  projectId: "compressio-78a31",
  storageBucket: "compressio-78a31.firebasestorage.app",
  messagingSenderId: "569817073799",
  appId: "1:569817073799:web:59c82b7a2cdc8fb8cfd022",
  measurementId: "G-S6DPL2CE71"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);