# Assisting Experts in Image Description for Visually Impaired People
This repository contains the code used during the development, experimentation and analysis steps of my Master Thesis at the TU Delft.

The aim is to help the KB National Library of the Netherlands, by improving the image description process for visually impaired people. Currently, this is a manual process, and our tool is a means to assist the experts writing these descriptions.


## Finding the thesis
For more information, you can find the thesis on the [TU Delft Repository](https://repository.tudelft.nl).

## Try it yourself
To try it, you can run the `combined.py` file (in the src folder), passing to it, as an argument, the name of the file you'd like to analyze. For example:
```
python combined.py wikipedia_WIT_dataset_file.gz
python combined.py some_dtbook_file.xml
```
If you want to run your image through Microsoft Azure Image Analysis, you need to add the API keys to your environment variables (as will be indicated by the error messages that are returned).

It is also possible to run only the image analysis. You can do this by running the `src/azure/azure.py` file with the image file name you'd like to analyze. For example:
```
python azure.py dog.jpg
```
## Just Azure
Microsoft has also put the analyze image service online, to be used freely, if the only thing you're interested in is the image analysis. You can find it [on this website](https://azure.microsoft.com/en-us/services/cognitive-services/computer-vision/#features).