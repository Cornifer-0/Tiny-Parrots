# 🦜 TinyParrot
Pol Creixans Comerma
  FIB, Computer Engineering student
Abel Riba Alcón
  ETSEIB, Industrial Engineering student




Inspiration: Private & Safe AI by Design
Most commercial "smart" toys rely on cloud computing, streaming children's photos and voice recordings across the internet to remote corporate servers. This centralized model is neither democratic nor safe, children's personal environments should never serve as data-harvesting pipelines for big tech databases. 
TinyParrot challenges this paradigm with an educational robotic companion built around Privacy by Design: 
100% Offline: All camera frames, audio samples, and machine learning inferences execute strictly on the local hardware. Zero personal data ever leaves the device. Safe & Regulation-Ready: Protects children in homes and classrooms by complying with European data protection standards and eliminating cloud vulnerabilities. 
How It Works
Active object inquiries: The camera continuously scans the environment. When TinyParrot detects a trained object that does not yet have a custom name assigned, it actively prompts the user by asking what it is. Recording voice labels: The user can teach the parrot the object's name by holding down Button B on the Modulino Buttons and speaking into the microphone. Releasing the button links that audio recording directly to the detected object ID. Autonomous identification: The next time TinyParrot spots that same object, it no longer asks for its name, it announces the custom voice label recorded by the user. 
2. User Experience & Playful Interactions 
To keep the educational experience friendly for children, several interactive elements are integrated: 
Chatter & sound effects: To give the parrot personality, it periodically plays short pre-recorded sound effects and voice lines. Pressing Button C on the Modulino Buttons feeds the tiny parrot. Status expressions: The LED matrix on the Arduino Uno Q board is programmed to display custom expressive emoticons based on the current state (such as searching, or successfully recognizing an object). Despite being inside the 3D-printed body, this serves as an internal visual indicator during development, testing, and debugging. 
Hardware Architecture & Assembly
The system is driven by the Arduino Uno Q. An internal USB Hub is used to bridge and route the multiple peripheral connections to the board. 
Audio & Vision Peripherals: 
Modulino Buttons: Positioned on the top of the head to control voice recordings and user interaction. 
Dual speakers: Integrated on the parrot's head, allows you to adjust the volume with a small wheel. USB webcam with integrated microphone: It’s quite bulky, but it provides us with both a camera and a microphone at the same time.. 
Power Management: 
Operates portably using an internal 5000 mAh USB-C Power Bank (5V/3A output), providing over 2 hours of use. Compatible with standard 5V wall adapters via the external USB-C port. 
Chassis & 3D Printing: 
The entire body is fabricated in PLA filament using desktop FDM 3D printing. 
Assembly & Practical Tips: 
The top aperture on the head allows the modulino buttons cable to connect directly down into the Uno Q and the speakers to the USB hub. 
Cable management: Because internal volume inside the bird is limited, it is strongly recommended to use short, flexible connection cables. 
Camera fixture: To keep the lens firmly centered, you can design a secondary 3D-printed mounting bracket. For an easier assembly, high-tack tape can also hold the camera securely in place 
 
Key Takeaway
Privacy by design: All machine learning inference happens on-device. Zero photos, video, or voice recordings are sent to external cloud servers. 
