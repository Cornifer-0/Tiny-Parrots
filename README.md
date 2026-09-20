🦜 TinyParrot — Private & Safe AI Companion
> **An educational robotic companion built with Privacy by Design.** 
> 100% offline machine learning that listens, learns, and interacts without ever sending your data to the cloud.
---
![Hardware](https://img.shields.io/badge/Hardware-Arduino_Uno_Q-008184?style=for-the-badge&logo=arduino&logoColor=white)
![Privacy](https://img.shields.io/badge/Privacy-100%25_Offline-brightgreen?style=for-the-badge)
![Compliance](https://img.shields.io/badge/Compliance-EU_Data_Protection-blue?style=for-the-badge)
![3D Printing](https://img.shields.io/badge/Chassis-FDM_3D_Printed-orange?style=for-the-badge)
---
👥 Project Creators
Creator	Role / Institution
Pol Creixans Comerma	Computer Engineering Student @ FIB (Facultat d'Informàtica de Barcelona)
Abel Riba Alcón	Industrial Engineering Student @ ETSEIB (Escola Tècnica Superior d'Enginyeria Industrial de Barcelona)
---
💡 Inspiration & Privacy by Design
Most commercial "smart" toys rely on cloud computing, constantly streaming children's photos and voice recordings across the internet to remote corporate servers. This centralized model is neither democratic nor safe—children's personal environments should never serve as data-harvesting pipelines for big tech databases.
TinyParrot challenges this paradigm by introducing an educational robotic companion built strictly around Privacy by Design:
🔒 100% Offline: All camera frames, audio samples, and machine learning inferences execute locally on the hardware. Zero personal data ever leaves the device.
🛡️ Safe & Regulation-Ready: Protects children in homes and classrooms by aligning with European data protection standards and completely eliminating cloud-based vulnerabilities.
> [!IMPORTANT]
> **Key Takeaway:** All machine learning inference happens on-device. Zero photos, videos, or voice recordings are ever sent to external cloud servers.
---
⚙️ How It Works
```
   ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
   │ 1. Active Scan  │  ──>  │ 2. Voice Label  │  ──>  │ 3. Autonomous   │
   │ Detects Unnamed │       │ User teaches    │       │ Identification  │
   │ Object & Asks   │       │ name via Button │       │ Speaks learned  │
   └─────────────────┘       └─────────────────┘       │ name on sight   │
                                                       └─────────────────┘
```
Active Object Inquiries: The camera continuously scans the environment. When TinyParrot detects a trained object that does not yet have a custom name assigned, it actively prompts the user by asking what it is.
Recording Voice Labels: The user can teach the parrot the object's name by holding down Button B on the Modulino Buttons and speaking into the microphone. Releasing the button links that audio recording directly to the detected object ID.
Autonomous Identification: The next time TinyParrot spots that same object, it no longer asks for its name—it announces the custom voice label previously recorded by the user.
---
🎮 User Experience & Interactive Features
To keep the educational experience engaging and friendly for children, TinyParrot includes several interactive elements:
🔊 Chatter & Sound Effects: To give the parrot personality, it periodically plays short pre-recorded sound effects and voice lines.
🍓 Interactive Feeding: Pressing Button C on the Modulino Buttons "feeds" the tiny parrot.
🤖 Status Expressions: The LED matrix on the Arduino Uno Q board is programmed to display custom expressive emoticons based on the current state (e.g., searching, successfully recognizing an object).
> *Note: While housed inside the 3D-printed body, the LED matrix serves as a vital internal visual indicator during development, testing, and debugging.*
---
🛠️ Hardware Architecture & Assembly
The system is powered by the Arduino Uno Q, utilizing an internal USB Hub to bridge and route peripheral connections.
```
                  ┌───────────────────────────────┐
                  │        Arduino Uno Q          │
                  └──────────────┬────────────────┘
                                 │
                          ┌──────┴──────┐
                          │   USB Hub   │
                          └──────┬──────┘
         ┌───────────────────────┼───────────────────────┐
         ▼                       ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Modulino        │     │  Dual Speakers  │     │ USB Webcam +    │
│ Buttons (Head)  │     │  (Volume Wheel) │     │ Microphone      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```
Component Breakdown
Subsystem	Component	Function & Details
Main Processing	Arduino Uno Q	Core microcontroller running all local ML logic & state loops.
Control	Modulino Buttons	Positioned on top of the head for voice recording & direct interaction.
Audio Output	Dual Speakers	Mounted on the head; includes a physical wheel to adjust volume.
Vision & Audio In	USB Webcam + Mic	All-in-one peripheral providing camera feed and voice input.
Power Management	5000 mAh USB-C Power Bank	Provides 5V/3A output for over 2 hours of continuous portable use.
	External USB-C Port	Allows direct powering via standard 5V wall adapters.
---
🖨️ Chassis & 3D Printing
Fabrication: The entire body is printed using standard PLA filament on a desktop FDM 3D printer.
Cable Routing: A top aperture on the head allows the Modulino Buttons cable to connect directly down to the Uno Q, while the speakers route to the internal USB hub.
💡 Assembly & Practical Tips
Cable Management: Because internal volume inside the bird is limited, it is strongly recommended to use short, flexible connection cables.
Camera Mount: To keep the lens firmly centered, you can design a secondary 3D-printed mounting bracket. For a quicker assembly during testing, high-tack tape also holds the camera securely in place.
---
<p center align="center">
  <i>Developed for private, decentralized, and safe educational computing.</i>
</p>
