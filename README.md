# K-Verse - Virtual Reality, Physical Consequences

![Tracking System](https://github.com/Mallington/Bath-Hack-2022-Backend/blob/master/docs/tracking.jpg)

## What it does

We've built a full-fledged VR shooter called K-Verse, your mission is to take out the sentient turrets in-game. You can dodge the bullets and even shoot back!

The physical real-world nerf turret tracks the player's movements using AI, ML, Insert Buzz Word and when you are hit in-game, it fires at will! The combination of immersive VR and physical hits in the real world makes for a thrilling experience.
## How we built it

We created the VR game in Unreal engine, this was pretty straightforward, although it did mean transporting a whole gaming PC to campus.

The nerf turret is made from a nerf gun bought from the toy shop, hacked into submission, and its guts are taken out and reassembled. We are using an Arduino Uno for the low-level brains, it uses a Relay to switch the main power supply on and off. We are using a stepper motor and a mountain of cardboard to rotate it so that we can aim at the player.

![Nerf turret](https://raw.githubusercontent.com/Mallington/Bath-Hack-2022-Backend/master/docs/nerf-turret.jpg)

The Arduino is connected to a python backend that tracks players' movements using an onboard mounted webcam and hosts a rest service from which the Game can trigger the nerf gun to fire.

### See the frontend here: [Unreal VR Code](https://github.com/LukeHosk/BathHack2022)
