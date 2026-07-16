# Effects of Gender-Aware Language on Chatbot Interactions in CS Education
This repository contains the study materials for the experiment study presented in my Bachelor's thesis, which examines how gender-specific vs. gender-neutral language affects trust, perceived usefulness, and enjoyment and how the chatbot's communication style moderates the effect in educational chatbot interactions. 

## Table of Contents
- [Abstract](#abstract)
- [Materials](#materials)
  - [Rasa Chatbot](#rasa-chatbot)
  - [LimeSurvey](#limesurvey)
  - [Data Analysis](#data-analysis)
- [License](#license)

## Abstract
Chatbots are computer programs that simulate human conversation mainly through text messages. As chatbot applications in various areas continue to grow, they have become the subject of numerous studies. However, the effect of language used in chatbot interactions is still underresearched. To address this problem, this study explored whether the use of gender-specific or gender-neutral language in educational chatbots differently influences trust, perceived usefulness, and enjoyment. Additionally, we examined how the chatbot’s communication style alters these effects. A 2 x 2 between-subjects user study was conducted with N = 94 participants, where participants interacted with one of four custom Rasa chatbots during a coding mentorship session. The chatbots differed only in their language and communication style. The results revealed an interaction effect between language and communication style on trust, indicating higher trust when gender-specific language was combined with empathetic communication. By contrast, no significant main effect was found for language on any of the dependent variables. We conclude that language plays a greater role in building trust and that perceived usefulness and enjoyment are likely determined by other features, such as functionality and empathy level. The findings highlight the importance of linguistic design for establishing trust and contribute to a deeper understanding of linguistic elements in chatbot design.

## Materials
### Rasa Chatbot
To rebuild the Rasa chatbot, which was used for the study, please follow the steps in the [README](my-rasa-assistant-github/README.md) in the corresponding folder.

### LimeSurvey
You can recreate the survey by importing the provided [limesurvey_cs_chatbot_gender.lss](survey/limesurvey_cs_chatbot_gender.lss) file in [LimeSurvey](https://www.limesurvey.org).

### Data Analysis
Jupyter Notebooks for analysis are in the [data_analysis](data_analysis) folder. They can be uploaded e.g. in [Google Colab](https://colab.google) and modified for the own use. The required data for running the provided notebooks are available [here](survey/results-filtered-94.csv).

## License
The code (Rasa chatbot, code of GitHub pages website, and .ipynb notebooks) are licensed under the [MIT License](LICENSE).

The LimeSurvey materials (.lss) and the website content are licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
