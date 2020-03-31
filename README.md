# Course: Deep Learning for Marketing 
# Project: Brand Management 

The goal of this project is to replicate another project called 'Visual Listening' that compares how brands are perceived via images found on social media. 
In our project, the target is to build a webtool where the user can enter a brand, for example 'swatch', and receive a webpage that analysis swatch-images - found on Instagram on either 
the official swatch user-profile or as #swatch hashtag on images from different users - and gives out the probability of these images being perceived as either 'glamourous', 'rugged', 'healthy' or 'fun' (four categories). 

## Getting Started
```
1. download Github Desktop 
2. install Github Desktop 
3. go to Github repository: https://github.com/snoweZz/DLfM_BrandManagement
4. by now you have received an invitation from Vince to have the rights to edit this project
5. press the green button 'clone or download', press 'open in Desktop', this will clone this online repo to your local machine
into the directory Documents/Github/DLfM_BrandManagement
6. in Github Desktop, press 'current branch', then press 'new branch', name the branch like so 'Thibi-branch' 
7. make sure the tick is on 'Thibi-branch' which means that all that you are doing from now on will be tracked on that branch automatically
8. work on the project through command line, open cmd, cd to the directory Documents/Github/DLfM_BrandManagement
or you can also open and work on the project from spider, pycharm etc. by going to that same directory
9. change, edit, modeify, delete as you with - work on that project
10. afterwards, open github Desktop, you will see all changes there, they were tracked
11. commit changes: write in 5-10 words what changes you made in the 'summary' box, then hit 'commit to Thibi-branch' 
12. press 'push to origin' to upload all changes to the remote online Github repo https://github.com/snoweZz/DLfM_BrandManagement
```
### Repository

The folder structure of this repository is based on the following folders: 
- src: all code developed in .ipynb or .py
- data: all data needed to power the code frameworks
- model: all models built from code that served as machine for feeding in the data
- about: project files in pdf, word-doc etc. that describe the project
- other: code from other projects

### Prerequisites

What things you need to install the software and how to install them

```
to download images from Flickr, you need to install 
- Linux on Windows
- Java on Linux 
```

### Installing

A step by step series of examples that tell you how to get a development env running

```
to download images from Flickr, you need to install:  

- Download the latest JAVA SDK. You can do this as usual from your browser.
- Download from: http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html
-Open PowerShell, then type bash
-Within your bash terminal, copy the tgz file from /mnt/c/Users/<your windows username>/Downloads/jdk-8u131-linux-x64.tar.gz into /home/<your subsystem username/jdk-8u131-linux-x64.tar.gz
-Go back to your home folder: cd ~
-Extract the package: tar xvzf jdk-8u131-linux-x64.tar.gz
-Set the environment variables
-Open your bashrc file: sudo vim ~/.bashrc
-Add your java directory to the PATH and add JAVA_HOME right at the end.
-It will look like below:
  export PATH=~/jdk1.8.0_131/bin/:$PATH
  export JAVA_HOME=~/jdk1.8.0_131

```
```
to download images from Instagram, you need to run the following Jupyter notebooks 

- 01. Get_BrandNames_For_Images_Instagram
- 02. Get_Images_From_Instagram
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Caffe](https://caffe.berkeleyvision.org/) - The deep learning framework used

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [Github Desktop](https://desktop.github.com/) for versioning. For the versions available, see the branches of each group member. 

## Authors

* **Vince Rueegge**
* **Neeraj Kumar**
* **Theebana Rajendram**
* **Linda Samsinger** 


See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the UZH License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Code used from "Visual Listening" project 

