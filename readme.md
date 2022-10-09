# How to use this repo
**Do note, documentation is a WIP. I am writing this shit on a fucking hotel computer while I am out-of-town.**

## Finding your user id / chatroom id

- Go to your profile page, and go into inspect element. Search for the "network" tab.
> Note!!! If there is no network tab, you should 100% use a browser that has one, you NEED this to find it
- Look for "accounts" in the list of fetches. It should show up. If not, reload the page while staying on the network tab to refresh it.
- Look for the query of it. It *should* be in the url, and look for "ids". It should look like "ids=174873498173941". That number after the = sign is your account id.
> YOU NEED YOUR ACCOUNT ID TO USE ANY OF THESE WIDGETS
- Go into the actual data now of this. Look through the json for a key named "chatRoomId". Note that down as well, you will need that.

## How to actually use that data on this

- Replace the "chatroomId" or "userId" variables in any of the script tags of the html files to your individual ones

## How is this not a scam/etc.
- A.) that is too much effort and I'm lazy, and B.) this requires no authorization to access. You literally provide the user id or chatroom id, speaking of which, all of my own are here as well. I appreciate you fansly for making it pretty easy to do this.

## What's the "fuckyoucors" thing?
- Cors is the worst thing ever invented, so I have to create a proxy for all of the web requests that these files make so it actually gets the data, otherwise it will give a big red error (feel free to remove the cors thing if you don't believe me)

# Crediting

Credit is not required, but you're kinda a piece of shit if you don't, to be completely honest. I've spent like 9+ hours now and counting on vacation writing all of this shit out, for you to use for free.

Just shout-out any of my socials.
All of them (including fansly) are h3llo_wor1d, except for twitter, which is h31lo_wor1d.

Also feel free to link this repo!