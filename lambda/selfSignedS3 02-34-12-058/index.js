var AWS = require('aws-sdk');
var s3 = new AWS.S3({
    signatureVersion: 'v4',
});

exports.handler = (event, context, callback) => {
    let ts = Date.now();
    let date_ob = new Date(ts);
    let day = date_ob.getDate();
    let month = date_ob.getMonth() + 1;
    let year = date_ob.getFullYear();

    let hours = date_ob.getHours();
    let minutes = date_ob.getMinutes();
    let seconds = date_ob.getSeconds();

    const url = s3.getSignedUrl('putObject', {
        Bucket: 'loyalty-partner-handback-files',
        // Key: year + "-" + month + "-" + day  + "_" + hours + ":" + minutes + ":" + seconds + ".csv",
        Key: event.name,
        Expires: 60,
    });


    callback(null, url);
};
