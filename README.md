# imagedescriptions
This repository stores the code used for my master thesis. The system should help the dutch Royal Library (KB) to more easily describe the images included in various different documents of text, such as news articles and magazines. These entail short, single-sentence descriptions.

## Try it yourself
The first version of analysis is already present. To try it, you can run the `analyze.py` file (in the src folder), passing to it, as an argument, the name of the XML file you'd like to analyze. For example:
```
analze.py volcano.xml
```
Note that if the analysis via Microsoft Azure has been done before, it is not re-run. Instead, the results from the previous run are loaded from the `.json` file in the image folder. If you want to run images through Azure yourself, you'll need to add the API keys to your environment variables (as will be indicated by the error messages that are thrown).

## Just Azure
Microsoft has also put the analyze image service online, to be used freely, if the only thing you're interested in is the image analysis. You can find it [on this website](https://azure.microsoft.com/en-us/services/cognitive-services/computer-vision/#features). The information used (so far) in this project are the `Tags` and the caption in the `Description`.
