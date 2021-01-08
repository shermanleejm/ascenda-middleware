const AWS = require("aws-sdk");
const { Transaction } = require("./models/Transaction");

AWS.config.update({
    region: "ap-southeast-1",
    accessKeyId: process.env.ACCESS_KEY_ID,
    secretAccessKey: process.env.SECRET_KEY_ID,
});

const sqs = new AWS.SQS({ apiVersion: "2012-11-05" });
const queueUrl =
    "https://sqs.ap-southeast-1.amazonaws.com/731706226892/dbs-poll.fifo";

const params = {
    AttributeNames: ["SentTimestamp"],
    MaxNumberOfMessages: 10,
    MessageAttributeNames: ["All"],
    QueueUrl: queueUrl,
    VisibilityTimeout: 20,
    WaitTimeSeconds: 0,
};

const sqsReceiveMsg = () => {
    console.log("POLLING FOR MSG >>>>", new Date(Date.now()).toISOString());
    sqs.receiveMessage(params, async (err, data) => {
        if (err) {
            console.log("Receive Error", err);
        } else if (data.Messages) {
            data.Messages.forEach(async (msg) => {
                try {
                    const {
                        amount,
                        memberId,
                        outcomeCode,
                        transactionCode,
                    } = JSON.parse(msg.Body);

                    const [transaction] = await Transaction.findAll({
                        where: {
                            transactionCode: transactionCode,
                        },
                    });

                    if (transaction) {
                        transaction.amount = Number.parseFloat(amount);
                        transaction.outcomeCode = outcomeCode;
                        await transaction.save();

                        console.log("UPDATED TRANSACTION", transaction);
                    }
                } catch (e) {}

                const deleteParams = {
                    QueueUrl: queueUrl,
                    ReceiptHandle: msg.ReceiptHandle,
                };

                sqs.deleteMessage(deleteParams, function (err, data) {
                    if (err) {
                        console.log("Delete Error", err);
                    } else {
                        console.log("Message Deleted", data);
                    }
                });
            });
        }
    });
};

exports.sqsReceiveMsg = sqsReceiveMsg;
