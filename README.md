# STM32 VS Code Extension User Guide

## Table of Contents
- [Quick Start with Tutorial Videos](#quick-start-with-tutorial-videos) 
- [Feature description](#feature-description)  
	- [Create/import a project](#create-import-a-project)  
		- [Create an STM32CubeMX project](#create-an-stm32cubemx-project)  
		- [Create an empty project](#create-an-empty-project)  
		- [Import CMake project](#import-cmake-project)  
	- [Launch STMCUFinder](#launch-stmcufinder)  
	- [Upgrade STLINK firmware](#upgrade-stlink-firmware)  
- [Build a project](#build-a-project)  
	- [Select a build target](#select-a-build-target) 
	- [Add a build target](#add-a-build-target) 
	- [Start build](#start-build)  
		- [Build single core devices](#build-single-core-devices)
    	- [Build advanced devices](#build-advanced-devices)
- [Debug a project](#debug-a-project)  
	- [Debug single core devices](#debug-single-core-devices)
    - [Debug advanced devices](#debug-advanced-devices)
		- [Debug trust zone devices](#debug-trust-zone-devices)
		- [Debug dual core devices](#debug-dual-core-devices)
		- [Debug boot flash devices](#debug-boot-flash-devices)
	- [Create a new launch configuration](#create-a-new-launch-configuration)  
- [Flash a device](#flash-a-device)
- [Troubleshooting](#troubleshooting)  
	- [Build related issues](#build-related-issues)
	- [CMake versioning issue](#cmake-versionning-issue)  
	- [Clean build configuration](#clean-build-configuration)  
	- [Unable to start debugging](#unable-to-start-debugging)  
	- [Debug related issues](#debug-related-issues) 
	- [Advanced devices debug issues](#advanced-devices-debug-issues)
		- [Fail to launch debug](#fail-to-launch-debug)
		- [Handle multiple projects in one workspace](#handle-multiple-projects-in-one-workspace)
- [Migrate an STM32 based project to VS Code](#migrate-an-stm32-based-project-to-vs-code)
 
- [Tips and tricks](#tips-and-tricks)  
	- [Prevent popups](#prevent-popups)  
	- [Advanced debug with STM32CubeIDE](#advanced-debug-with-stm32cubeide)  
	- [Keep multiple STM32 VS Code extension versions installed](#keep-multiple-stm32-vs-code-extensions-versions-installed)

## Quick Start with Tutorial Videos

Get up to speed with the new version using our easy-to-follow tutorial videos: 
<div style="width: 300px;"> 

[![How to install the STM32 VS Code extension](./img/HowtoinstalltheSTM32VSCodeextension.jpg)](https://www.youtube.com/watch?v=DLmbNfUh62E)

[![How to create projects using STM32 VS Code Extension](./img/HowtocreateprojectsusingSTM32VSCodeExtension.jpg)](https://www.youtube.com/watch?v=DDVdq47Dd94)

[![How to debug using STM32 VS Code Extension](./img/HowtodebugusingSTM32VSCodeExtension.jpg)](https://www.youtube.com/watch?v=yasF8z0BCzM)
</div><br />

## Features description

### Create/import a project

The **STM32 VS Code** extension provides two distinct project creation options:
- **STM32CubeMX Project:**  This is an **STM32CubeMX** managed project relying on **CMake** as build system.

- **Empty Project:**  This is a barebone project setup. It includes the minimum code and scripts needed to bootstrap the STM32 device.

When a project is imported into **VS Code**, the extension autogenerates the **.vscode** folder, containing required metadata for edit/compile/debug, assuming that is not already existing in the project.

For a comprehensive guide, watch our tutorial video titled [**How to create projects using STM32 VS Code Extension**](https://www.youtube.com/watch?v=DDVdq47Dd94). It provides step-by-step instructions tailored for both new and experienced users.

#### Create an STM32CubeMX project  

The button **Launch STM32CubeMX** opens **STM32CubeMX** if it is installed. It allows the user to create, configure, and generate the initialization code for the selected device.
<div style="width: 1000px;"> 

![STM32CubeMX](./img/MX.svg) </div><br />

To create a project targeting **VS Code**, the user must select the toolchain to **CMake** in the project manager panel within **STM32CubeMX**.  
For further information on **STM32CubeMX**, refer to the [***UM1718***](https://www.st.com/resource/en/user_manual/um1718-stm32cubemx-for-stm32-configuration-and-initialization-c-code-generation-stmicroelectronics.pdf).
<div style="width: 1000px;"> 

![STM32CubeMX ProjectManager](./img/MXProjectManager.svg) </div><br />

**STM32CubeMX CMake generator** generates the following files when **CMake** is chosen as a toolchain:

- **cmake\\** folder: This folder contains **CMake** related files:
	- **stm32cubemx\" folder:** This contains the **CMakeLists.txt**. **STM32CubeMX** manages this file
	- **gcc-arm-none-eabi.cmake:** Generated only once by **STM32CubeMX**, the user owns and manages this file
- **CMakeLists.txt:** Generated only once by **STM32CubeMX**, the user owns and manages this **CMake** file
- **CMakePresets.json:** Generated only once by **STM32CubeMX**, the user owns and manages this file
- **STM32xxxxxxx_FLASH.ld:** A linker script. Ownership shared between **STM32CubeMX** and the user

The project created by **STM32CubeMX** does, at this point not contain the **.vscode** folder. The **STM32Cube VS Code extension** autocreates this metadata folder when importing the project using the **Import CMake project**.

#### Create an empty project 

This button generates a template project that includes the minimum set of source and metadata files needed to build a project, initialize the **MCU** and branch to **main()**. 
This project type is targeting end-users who need maximum flexibility, minimum dependencies, and full ownership.
It is fully up to the user to add **HAL/LL drivers** or write their own code and drivers from scratch.

When clicked, the user is prompted to enter a name for the project.
<div style="width: 1000px;"> 

![Create an empty project step 1](./img/EmptyPro1.svg) </div><br />  

After naming the project, the file explorer opens, allowing the user to browse and select a project directory.
<div style="width: 1000px;"> 

![Create empty project step 2](./img/EmptyPro2.svg) </div><br />

The next step is to select the target, which can be either a device or a board.
<div style="width: 1000px;"> 

![Create empty project step 3](./img/EmptyPro3.svg) </div><br />  

Afterwards, a project summary is presented, allowing the user to review the details before clicking on **Create project** or **Actions** to complete the project creation process.
<div style="width: 1000px;"> 

![Create empty project step 4](./img/EmptyPro4.svg) </div><br />  

At completed project creation, **VS Code** offers three options to the user for opening the new project:
- Adding the project to the currently opened window
- Opening a folder containing the project in a new **VS Code** session  <-- **Recommended** option
- Adding a link to the project in an existing workspace

***Tip:*** In the **VS Code C/C++** world, it is common practice to have one **VS Code** instance per project. This is a key difference vs **STM32CubeIDE**, which normally has several projects open inside one workspace. One project per **VS Code** instance ensures that the context for editor indexing, building and debugging works in the best way. Consequently, we recommend the second option.
<div style="width: 1000px;"> 

![Create empty project step 5](./img/EmptyPro5.svg) </div><br />

The project structure generated by the **STM32 VS Code extension** is as follows:
- **.vscode**\ folder:  A metadata folder containing:
	- **c_cpp_properties.json:** This file ensures that the **C/C++** editor indexing works properly
	- **extensions.json:** This file provides additional extension recommendations
	- **launch.json:** This file automatically generates debug configurations
	- **tasks.json:** This file is a template for executing certain tasks, such as flash loading
- **cmake**\ folder: This folder contains **CMake** related files:
	- **vscode_generated.cmake:** This is a converter-generated file. Only the **STM32 VS Code extension** manages this file
	- **gcc-arm-none-eabi.cmake:** Generated only once by the **STM32 VS Code extension**, the user owns and manages this file
- **Inc**\ folder: This folder is empty. It is up to users to add their own **header** files
- **Src**\ folder: This folder contains the **main.c**, the **syscall.c**, and the **sysmem.c** files. The users can add their own **source** files in this folder
- **Startup**\ folder: This folder contains the startup file **startup_stm32xxxxxxxx.s**
- **CMakeLists.txt:** Generated only once by the **STM32 VS Code extension**, the user owns and manages this **CMake** file
- **CMakePresets.json:** Generated only once by the **STM32 VS Code extension**, the user owns and manages this file
- **STM32xxxxxxx_FLASH.ld:** A linker script. Owership is shared between the **STM32 VS Code extension** and the user

<div style="width: 1000px;"> 

![Empty project structure](./img/EmptyProStruct.svg) </div><br />

#### Import CMake project

This feature allows the user to import a **CMake** project (**Empty project** or **STM32CubeMX** generated) into **VS Code**.  
The importer checks if the project already contains the **json-files** required to do **edit/compile/debug**. If these files do not yet exist, the extension generates them.

**NOTE:**   
Opening the project in **VS Code** through **File -> Open Folder** instead of using the **STM32 VS Code** extension's **Import CMake project** does not autogenerate the **json-files**.

<div style="width: 1000px;"> 

![Import CMake project step 1](./img/ImportPro1.svg) </div><br />

Afterwards, a project summary is presented to the user, allowing them to review the details before clicking on **Import project** or **Actions** to complete the process.
<div style="width: 1000px;"> 

![Import CMake project step 2](./img/ImportPro2.svg) </div><br />

At completed project import, **VS Code** offers three options to the user for opening the project:
- Adding the project to the currently opened window
- Opening a folder containing the project in a new **VS Code** session
- Adding a link to the project in an existing workspace
<div style="width: 1000px;"> 

![Import CMake project step 3](./img/ImportPro3.svg) </div><br />

### Launch STMCUFinder  

This button opens **ST-MCU-FINDER** if installed and allows the user to browse through the extensive range of **STM32** and **STM8** microcontrollers, microprocessors, development boards, and examples.
For further information on **ST-MCU-FINDER-PC**, refer to the [***DB3190***](https://www.st.com/resource/en/data_brief/st-mcu-finder-pc.pdf).
<div style="width: 1000px;"> 

![ST-MCU-FINDER-PC](./img/Finder.svg) </div><br />

### Upgrade STLINK firmware

This feature allows the user to upgrade the firmware of a device or board through the **USB** port.

**Hint:** Updating the **ST-LINK firmware** is required on many boards before the first debug launch!

<div style="width: 1000px;"> 

![STLINK firmware upgrade](./img/STLinkFWUpgrade.svg) </div><br />

**NOTE:** 
The **Upgrade STLINK firmware** can also be initiated from the **VS Code Command Palette**. Press **Ctrl + Shift + P** simultaneously, type **stm32**, and select **STM32 VS Code Extension: Upgrade STLINK firmware**.
<div style="width: 1000px;"> 

![STLINK firmware upgrade via Command palette](./img/STLinkFWUpgradeCmdPalette.svg) </div><br />

## Build a project

### Select a build target

To choose a build target:
- Access the **VS Code Command Palette** either through the settings or by using the keyboard shortcut **Ctrl + Shift + P**  
- Search for **CMake Preset** and choose **Select Configure Preset**
<div style="width: 1000px;"> 

![Select a build target step 1](./img/SelectBuild.svg) </div><br />

- Complete the process by choosing the build target.
<div style="width: 1000px;"> 

![Select a build target step 2](./img/SelectBuild2.svg) </div><br />

**NOTE:**  
Alternatively, you can use the CMake extension directly and choose a build target as demonstrated in the figure below.
<div style="width: 1000px;"> 

![Select a build target with CMake](./img/CMakeSelectBuild.svg) </div><br />

### Add a build target

To add a build target, start by:
- Access the **VS Code Command Palette** either through the settings or by using the keyboard shortcut **Ctrl + Shift + P**  
- Search for **CMake Preset** and choose **Add configure Preset**
<div style="width: 1000px;"> 

![Add build target step 1](./img/AddBuild.svg) </div><br />

- Choose one of the options and follow the remaining steps to select the desired build target
<div style="width: 1000px;"> 

![Add build target step 2](./img/AddBuild2.svg) </div><br />

### Start build

#### Build single core devices

To build the project, click on the **Build** option, as illustrated in the picture below. The output console displays the build results.
<div style="width: 1000px;"> 

![Build a project](./img/Build.svg) </div><br />

#### Build advanced devices

The build process for single-core devices is identical to that for advanced devices, such as those with **TrustZone**, **Dual-Core**, or **BootFlash** capabilities. Simply click the build option, and CMake automatically initiates the build for all subprojects. The figure below illustrates an example of building a **dual core** device.
<div style="width: 1000px;"> 

![Build an advanced project](./img/BuildAdvanced.svg) </div><br />

## Debug a project

For a quick introduction on project debugging, watch our tutorial video [**How to debug using STM32 VS Code Extension**](https://www.youtube.com/watch?v=yasF8z0BCzM). It provides step-by-step instructions tailored for new users.

### Debug single core devices
The **launch.json** file contains information about the debug configuration. 
The extension creates two default debug configurations for the case of single core devices:
- **Build & Debug Microcontroller - ST-Link**: This option relies on **CMake** and allows you to build the code, load it onto the microcontroller, and initiate debugging.
- **Attach to Microcontroller - ST-Link**: This option relies on **CMake** and allows you to connect the debugger to a running target without downloading new firmware.

Users have the option to modify and create their own configuration by editing the **launch.json** file. Additional details on creating a new launch configuration can be found in the relevant section.

**NOTE:**  
We recommend updating the **STLINK firmware** prior to initiating the debug process to prevent potential problems. For additional information, refer to the section titled [Unable to start debugging](#unable-to-start-debugging).

To launch debugging, choose a launch configuration and click on the **start** button. At this stage, users can observe **local** and **global variables**, include expressions in the **watch stack**, set **breakpoints**, and view **peripheral registers**.  
<div style="width: 1000px;"> 

![Launch debug](./img/Debug1.svg) </div><br />

### Debug advanced devices
#### Debug trust zone devices
For the case of Trust Zone devices, the extension creates six default debug configurations:
- **Build & Debug Secure Microcontroller - ST-Link**: This option allows you to load the code onto the **Secure** microcontroller, and initiate debugging. 
- **Attach to Secure Microcontroller - ST-Link**: With this option, you can connect the debugger to the **Secure** core without downloading new firmware.
- **Build & Debug NonSecure Microcontroller - ST-Link**: This option allows you to load the code onto the **NonSecure** microcontroller, and initiate debugging. 
- **Attach to NonSecure Microcontroller - ST-Link**: With this option, you can connect the debugger to **NonSecure** core without downloading new firmware.
- **Build & Debug Microcontroller Secure and NonSecure- ST-Link**: This option allows you to load the code onto the **Secure** and **NonSecure** microcontroller, and initiate debugging. 
- **Attach to Microcontroller Secure and NonSecure- ST-Link**: With this option, you can connect the debugger to both the **Secure** and **NonSecure** without downloading new firmware.

**NOTES:**
- Projects generated with **STM32CubeMX**, use **Build & Debug Microcontroller Secure and NonSecure - ST-Link**. Also, use **Attach to Microcontroller Secure and NonSecure - ST-Link**. This is recommended because the secure code transitions to non-secure code by default. Debugging or attaching to **secure** or **non-secure** code separately causes a hard fault.
- **STM32Cube VSCode extension** does not support option bytes settings. To set the **TrustZone** option byte, use [***STM32CubeProgrammer***](https://www.st.com/en/development-tools/stm32cubeprog.html) tool.

<div style="width: 1000px;"> 

![Launch debug TZ1](./img/DebugTZ1.svg) </div><br />

#### Debug dual core devices
In the case of dual core devices, the extension creates three default debug configurations:
- **Debug CM7- ST-Link**: This option allows you to load the code onto the microcontroller, and initiate debugging. 
- **Attach CM7 - ST-Link**: With this option, you can connect the debugger to **CM7** core without downloadig new firmware.
- **Attach CM4 - ST-Link**: With this option, you can connect the debugger to **CM4** core without downloadig new firmware.

**NOTE:**
**STM32CubeMX** and most **STM32Cube examples** for **dual-core** devices configure **CPU1** to control **CPU2's** launch. The master-slave setup requires **CPU1** to run code to make **CPU2** accessible to the debugger. Therefore, we recommend debugging **CPU1** first, then attaching **CPU2**.

<div style="width: 1000px;"> 

![Launch debug Dual core](./img/DebugDualCore.svg) </div><br />

#### Debug boot flash devices
In the case of boot flash devices, the extension creates two default debug configurations:
- **Debug external memory- ST-Link**: This option allows you to load the code onto the **external memory**, and initiate debugging.
- **Attach external memory - ST-Link**: With this option, you can connect the debugger to an **external memory** without downloadig new firmware.
<div style="width: 1000px;"> 

![Launch debug ExtMem](./img/DebugExtMem.svg) </div><br />

### Create a new launch configuration

To create a new launch configuration, follow these steps:

- Open **Run and Debug**
- Access the **launch.json** file
- Click on **Add configuration**
- Choose the desired launch type
- Adjust the settings to match your configuration
<div style="width: 1000px;"> 

![Add launch configuration step 2](./img/AddDebug.svg) </div><br />

- Save the **launch.json** file to add the new launch configuration
<div style="width: 1000px;"> 

![Add launch configuration step 2](./img/AddDebug2.svg) </div><br />

## Flash a device
If you decide to flash the device without debugging, you can use **VS Code** Tasks. To access this feature, click on Terminal and then select "Run Task." Alternatively, use the Command Palette by typing **Ctrl + Shift + P**, then select **Run Task** and press **Enter**. A list of flashing options is then displayed. These tasks are retrieved from the **tasks.json** file, which is generated by the **STM32Cube VS Code extension**.
<div style="width: 1000px;"> 

![Flash a device](./img/FlashDevice.svg) </div><br />

## Troubleshooting

### Build related issues 

#### CMake versioning issue

If you have multiple software or tools that utilize **CMake**, there is a chance that **VS Code** could reference an incorrect version required by the extension. If this occurs, you might experience a build error with a message stating, **CMake 3.22 or higher is required. You are running version x.y.z**.
<div style="width: 1000px;"> 

![CMake versioning issues](./img/CMakeIssues.svg) </div>

To overcome this issue:  

- Close **VS Code**
- Access the environment variable settings on your operating system and confirm that the **STM32CubeCLT_PATH** is set correctly
- Relaunch **VS Code** and continue with the project build process

<br />

#### Clean build configuration

In cases where a project was compiled using older versions of **STM32CubeMX**, **STM32CubeCLT**, or the extension itself, rebuilding the project may sometimes fail. 
To prevent or resolve this issue, open the **VS Code Command Palette** either through the settings or by using the keyboard shortcut **Ctrl + Shift + P** and search for **CMake: Delete Cache and Reconfigure**.
<div style="width: 1000px;"> 

![Resolve build issues](./img/BuildIssues.svg) </div><br />

### Unable to start debugging

If the debugger fails to connect to the board, first refer to the debug console to check the root cause. If you see a message that says **Error in initializing STLINK device. Reason: STLINK firmware upgrade required**, just click on the **Upgrade STLINK firmware** feature to overcome this issue.
<div style="width: 1000px;"> 

![Unable to start debugging](./img/ErrorFWUpgrade.svg) </div><br />

**NOTE:** 
The **Upgrade STLINK firmware** can also be initiated from the **VS Code Command Palette**. Press **Ctrl + Shift + P** simultaneously, type **stm32**, and select **STM32 VS Code Extension: Upgrade STLINK firmware**.

### Debug related issues

When it comes to large and complex projects, users may encounter some issues while attempting to debug their **STM32CubeMX** generated application on their own PCB.

Our recommendation is to create a new [**empty project**](#create-an-empty-project) that only contains the minimal set of source files needed to bootstrap the **MCU**.
If the project compiles, flashes, and debugs on the device, the remaining issues likely arise from STM32CubeMX generated code, user code, or option byte mismatches.

<br />

### Advanced devices debug issues
#### Fail to launch Debug
If debugging advanced devices like **TrustZone**, **dual-core**, or **boot flash** fails with a message saying **STM32VSCodeExtension.<Target> is not set**, it means the **Loadfiles** values in the **launch.json** file are deprecated and need to be recalculated.

<div style="width: 1000px;"> 

![Advanced devices Debug Issues 1](./img/AdvancedDebugIssues1.svg) </div><br />
The **STM32Cube VS Code extension** provides a shortcut to recalculate these values. To resolve this issue, access the Command Palette with **Ctrl + Shift + P**, type **stm32**, and select **STM32 VS Code Extension: Update CMake Information**.
<div style="width: 1000px;"> 

![Advanced devices debug Issues 2](./img/AdvancedDebugIssues2.svg) </div><br />

#### Handle multiple projects in one workspace
When multiple projects are open in one workspace, the debugger may fail to detect which project to work on. In such cases, use the **STM32 VS Code Extension: Update CMake Information** feature to force the debugger to use a specific project.
<div style="width: 1000px;"> 

![Handle multiple projects in one workspace step 1](./img/MultiProInOneWS1.svg) </div><br />
<div style="width: 1000px;"> 

![Handle multiple projects in one workspace step 2](./img/MultiProInOneWS2.svg) </div><br />

## Migrate an STM32 based project to VS Code

Migrating a project from one tool to another is not a complex task, but it does require a specific sequence of steps to be followed.  
The number of steps needed for the migration varies depending on the original starting point of the project and the tools it relies on. 
In general, the migration process can be divided into three categories. Identify the category that best fits your project to ensure a successful migration.

- **Category 1:** The project was created using **STM32CubeIDE/MX** and managed by version 1.0.0 of the **STM32 VS Code extension**
- **Category 2:** The project was created using **STM32CubeIDE/MX** but was not migrated to version 1.0.0 of the **STM32 VS Code extension**
- **Category 3:** The project was not generated using **STM32CubeIDE/MX**. In this case, there are two possible solutions:
	- If the project uses **CMake**, you can import it by clicking on the [**Import CMake project**](#import-cmake-project) button
	- If the project does not use **CMake**: 
		- Create an empty project by clicking on the [**Create empty project**](#create-an-empty-project) button 
		- Transfer all the files and build settings to the **CMake-based empty project**

To migrate a project based on **category 1** or **category 2** to the new **VS Code** solution, follow the steps below.

1. Prerequisites  

Make sure to have **STM32CubeMX v6.11.0**, **STM32CubeIDE v1.15.0**, and **STM32CubeCLT v1.15.0** or newer versions installed.

2. Make a back-up 

Whenever updating any tool or embedded software, it is advisable to create a restore point or backup copy in case the outcome of the upgrade or migration is unsatisfactory.  Our recommendation is to either make a **commit/tag** in your repository or create a backup of the entire project.

3. Update **STM32CubeMX** and **STM32Cube firmware**

The migration may require upgrading to a new version of **STM32CubeMX**, which could introduce new **HAL drivers** or slight variations in code generation.  
Before proceeding to migrate the project to a **native CMake project**, make sure that the build and debug results within **STM32CubeIDE** are as expected after the updates. To do so:  

	3.1 Open the project with STM32CubeIDE v1.15.0 or newer version
	3.2. Open the STM32CubeMX ioc-file, and migrate your project to rely on a new STM32Cube firmware package if such is available  
    3.3. Regenerate the code  
	3.4. Build and debug the project with STM32CubeIDE  
<div style="width: 1000px;"> 

![Ioc migration](./img/IOCMigration.svg) </div><br />

If these steps have been completed without any issues, close **STM32CubeIDE** as the remaining part of the migration process is carried out on the file system.

4.  Delete old files

Due to the conceptual changes introduced by the new **STM32CubeMX** and **VS Code** solution, it is necessary for the user to remove certain project-related metadata manually.  
**STM32CubeMX** generates again the corresponding metadata in the subsequent step and further enhanced by the updated version of the **VS Code extension**. The code itself remain unaltered.  

**_Before proceeding with the deletion of metadata files, we recommend creating a backup restore point of the project._**   

a. If your project has only been accessed through **STM32CubeIDE** and not yet opened with the **STM32 VS Code for extension**, remove the following files:  

	a.1. .settings/ : folder containing some metadata
	a.2. .cproject : file containing build configuraitons for STM32CubeIDE
	a.3. .project : file containing project natures and paths to c/h folders and/or files

b. If your project has been previously utilized with both **STM32CubeIDE** and the **STM32 VS Code extension 1.0.0**, delete the following files in addition to the ones mentioned earlier:  

	b.1. .vscode folder
	b.2. build folder
	b.3. cmake folder
	b.4. CMakeLists.txt
	b.5. CMakePresets.json
	b.6. nvcpkg_configuration.json

After the removal of the specified files, start recreating the new **CMake-based** build structure. Only **STM32CubeMX** manages this new structure.

5. Generate **CMake** projects with **STM32CubeMX**

To proceed with the migration process, follow the steps given below:

	5.1. Launch STM32CubeMX 6.11.0 or a newer version (in stand-alone mode, not inside STM32CubeIDE)  
	5.2. Load the project that you intend to migrate  
	5.3. Access the project manager panel  
	5.4. Switch the "Toolchain / IDE" from "STM32CubeIDE" to "CMake"  
	5.5. Click on the "GENERATE CODE" button  

<div style="width: 1000px;"> 

![Generate CMake STM32CubeMX](./img/GenerateCMakeMX.svg) </div><br />

**STM32CubeMX CMake generator** generates the following files when **CMake** is chosen as a toolchain:

- **cmake\ folder:** This folder contains **CMake** related files:
	- **stm32cubemx\" folder:** This contains the **CMakeLists.txt**. Only **STM32CubeMX** manages this file
	- **gcc-arm-none-eabi.cmake:** Once generated by **STM32CubeMX**, the user can edit this file
- **CMakeLists.txt:** Once generated by **STM32CubeMX**, the user owns and manages this file
- **CMakePresets.json:** Once generated by **STM32CubeMX**, the user owns and manages this file
- **STM32xxxxxxx_FLASH.ld:** A linker script generated by **STM32CubeMX** indicating that **CMake** is selected as the toolchain

You can now compile your project via the command line by entering the following commands sequentially:
```
PROJ_FOLDER$> cmake -B build -G Ninja
PROJ_FOLDER$> cmake --build build -j
```
<div style="width: 1000px;"> 

![Build a project using CLI](./img/BuildCLI.svg) </div><br />

6. Set up the new **VS Code** environment

**_For users that are new to VS Code, it can be beneficial to use the **profiles** concept in VS Code to sandbox the STM32 environment into its own profile. Read more [***here***](https://code.visualstudio.com/docs/editor/profiles)._** 

To import the project to **VS Code**, follow the steps given below:

	6.1. Open VS Code and install the new extension version 2.0.0 which works with the new STM32CubeMX 6.11.0 or later and STM32CubeCLT 1.15.0 or later.
	6.2. Use the button/command "Import local project", point to your STM32CubeMX generated project folder.
<div style="width: 1000px;"> 

![Import migrated project](./img/ImportMigratedPro.svg) </div><br />

Once the project is imported, the **VS Code** extension automatically generates the files listed below:
- **.vscode\ folder:**  A metadata folder containing:
	- **c_cpp_properties.json:** This file ensures that the **C/C++** editor indexing works properly
	- **extensions.json:** This file provides additional extension recommendations
	- **launch.json:** This file automatically generates debug configurations
	- **tasks.json:** This file is a template for executing certain tasks, such as flash loading

**NOTE:**  

When opening a project in **VS Code** for the first time, you might encounter several prompts, such as:
- Select the **CMake preset:** Select the **Debug** preset  
- Install **Better C++ Syntax:** A highly beneficial extension for highlighting **C** and **C++** syntax  
- Configure **CMake options visibility:** Customize your view with the **cmake.options** property in settings

7. Add your **private folders source path** in the new generated **CMakeList.txt** file

If your project contains a private folder, it is crucial to include its path in the CMakeList.txt file.
<div style="width: 1000px;"> 

![Private folders source path in CMAkeLists](./img/CMakeListsPrivatePaths.svg) </div><br />

8. Update the CMake file to use the linker script that already existed in the project if needed:

This can be modified in the **\cmake\gcc-arm-none-eabi.cmake** file. Example:  
```
	set(CMAKE_C_LINK_FLAGS "${CMAKE_C_LINK_FLAGS} -T \"${CMAKE_SOURCE_DIR}/STM32F407VGTx_FLASH.ld\"")
```

9. Build & debug the project

For further details, refer to the sections titled [**Build a project**](#build-a-project) and [**Debug a project**](#debug-a-project).

For advanced debug features, we recommend using **STM32CubeIDE** side by side as a **debugger tool**. For further details, check [**Advanced debug with STM32CubeIDE**](#advanced-debug-with-stm32cubeide).

10. Congratulations! You are now set up. You can update your configuration in **STM32CubeMX** at any time. The generated **CMake** files and the source code function correctly within **VS Code**.

<br />

## Tips and tricks  

### Prevent popups

When you open some external websites that are referred to in resources, **VS Code** may prompt you since it does not automatically trust them.  
To avoid this prompt, open **Configure Trusted Domains** and trust the desired domains.
<div style="width: 1000px;"> 

![Configure trusted domains](./img/TipPopUp.svg) </div><br />

### Advanced debug with **STM32CubeIDE**

If you need advanced debug features that are not available in **VS Code**, you can use **STM32CubeIDE** as a **debugger tool** alongside it.  
To do this, you need to import the **elf-file** created by the project from **VS Code** into **STM32CubeIDE**. Doing so gives you access to all the basic and advanced debugging features of **STM32CubeIDE**. 
Despite not importing the **C/C++** code, source code lookup still functions correctly. This approach allows you to combine the strengths of both tools and enables you to edit, compile, and debug with **VS Code** while utilizing advanced debugging features with **STM32CubeIDE**.

To get started, open **STM32CubeIDE** and select **File > Import > C/C++ > STM32 Cortex®-M executable**.
<div style="width: 1000px;"> 

![Advanced debug step 1](./img/AdvancedDebug1.svg) </div><br />

Then, browse and select the elf file and specify the target device.
<div style="width: 1000px;"> 

![Advanced debug step 2](./img/AdvancedDebug2.svg) </div><br />

If necessary, edit the launch configuration and click on **Debug**.
<div style="width: 1000px;"> 

![Advanced debug step 3](./img/AdvancedDebug3.svg) </div><br />

That is it! Now, you can use **STM32CubeIDE's** advanced debug features.
<div style="width: 1000px;"> 

![Advanced debug step 4](./img/AdvancedDebug4.svg) </div><br />

### Keep multiple STM32 VS Code extensions versions installed

To retain a previous version of the **STM32 VS Code extension** while installing the latest version, you need to create a new profile by following the steps below:

- Navigate to the **VS Code** profiles and create a **new profile**
- Assign a name to the profile and complete the process by selecting **Create**
<div style="width: 1000px;"> 

![Create a profile](./img/CreateProfile.svg) </div><br />
- Proceed to install the latest version of the **STM32 VS Code extension** after creating the profile
- Now, you have two profiles; one contains **v1.0.0**, and the other contains **v2.0.0**
<div style="width: 1000px;"> 

![Profile for v1](./img/Profilev1.svg) </div><br />
<div style="width: 1000px;"> 

![Profile for v2](./img/Profilev2.svg) </div><br />

For users that are new to **VS Code**, read more about profiles [***here***](https://code.visualstudio.com/docs/editor/profiles). 

