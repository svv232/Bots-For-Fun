const login = require("facebook-chat-api");
var creds = require("./config.js");
 
// Create simple echo bot 
login({email: creds.email, password: creds.password}, (err, api) => {
    if(err) return console.error(err);
 
    api.listen((err, message) => {
        api.sendMessage(message.body, message.threadID);
    });
});
