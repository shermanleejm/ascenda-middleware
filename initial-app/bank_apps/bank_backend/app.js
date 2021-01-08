const express = require("express");
const bodyParser = require("body-parser");
require("dotenv").config();

const app = express();
const transactionRoutes = require("./routes/transaction");
const { sqsReceiveMsg } = require("./sqs");
// allows app to parse json
app.use(bodyParser.json());
// prevent CORS error
// Access Control Allow Origin states which domains can access your service. Putting a * means you let ANY domains access your service
app.use((req, res, next) => {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader(
        "Access-Control-Allow-Methods",
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE"
    );
    res.setHeader(
        "Access-Control-Allow-Headers",
        "Content-Type, Authorization"
    );
    next();
});

app.use("/", transactionRoutes);

setInterval(sqsReceiveMsg, 3000);

app.listen(8080);
