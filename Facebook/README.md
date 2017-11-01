- There were inside jokes from my friends back in Texas and this silly Facebook app keeps us laughing even though we are all spread across the country for college

- I used Heroku and Flask to deploy with some help from Hartley Brody and his excellent Blog Post https://blog.hartleybrody.com/fb-messenger-bot/

 - There were some issues:
    I wanted to use this for groupchats but fb requires a fully deployed
    and public application with legal documents for this to happen (which makes sense)

- My solution is to use their npm library and redeploy this whole thing in JavaScript
    so I can use this in actual group messages instead of this being a facebook page,
    and me adding testers to the app.
