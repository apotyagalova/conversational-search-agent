## Conversational search agent

A temporary repository of our ECIR 2024 accepted paper - A Conversational Search Framework for Multimedia Archives.

## Description

We describe a framework to enable multimodal conversational search for use with multimedia archives. Our current prototype demonstrates the use of an AI assistant during the multimedia information retrieval process for both image and video collections

## Getting Started
We take Flickr30k and MSR-VTT datasets for image and video search 
### Dependencies

* python 3.8
* rasa 3.6
* pandas 1.4.3
* flask 3.0.0
* whoosh 2.7
* numpy 1.19

### Executing program

* How to run the framework locally
* Run the Rasa server in the first command line window
```
rasa run --model models --enable-api --cors "*"
```
* Run the Rasa actions server in the second command line window
```
rasa run actions
```
* Run the Flask interface in the third command line window
```
python app.py
```
* Run the local server for displaying images or videos in the fourth command line window (only for the local version)
```
python -m http.server 8000
```
Live version is available here: http://34.252.91.139/

## Authors
Anastasiia Potiagalova,
Anastasia.Potyagalova2@mail.dcu.ie;

Gareth Jones,
Gareth.Jones@dcu.ie
## Version History

* 0.1
    * Initial Release


## Acknowledgments

This work was conducted with the financial support of the Science Foundation Ireland Centre for Research Training in Digitally-Enhanced Reality (d-real) under Grant No. 18/CRT/6224, and partially as part of the ADAPT Centre at DCU (Grant No. 13/RC/2106\_P2) (\url{www.adaptcentre.ie}). For the purpose of Open Access, the author has applied a CC BY public copyright licence to any Author Accepted Manuscript version arising from this submission. 

