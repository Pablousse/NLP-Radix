<!-- PROJECT TITLE -->
<p align="center">
  <h1 align="center">Resume parsing - Radix</h3>
</p>
<br />

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#installation">Installation</a>
    </li>
    <li><a href="#contributing">data sources</a></li>
    <li><a href="#contributing">Contributing</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

This project aims to compare resume and find the most similar ones.
The first part is to extract informations from the resume database and create a dataset.
The second part is to create a model that compare the different resumes (not implemented yet)

### Built With

* [Python 3.8.10](https://www.python.org/)

<!-- GETTING STARTED -->

### Installation

1. Clone the repo
   ```sh
   git clone git@github.com:Pablousse/NLP-Radix.git
   ```

2. Install dependencies
   ```sh
   pip install -r requirements.txt
   python3 -m spacy download en_core_web_sm
   ``` 

<!-- DATA SOURCES -->
## Data sources

You can find the data we worked with on :
<a href="https://github.com/arefinnomi/curriculum_vitae_data" rel="nofollow">Curriculum Vitae</a>

<!-- CONTRIBUTING -->
## Contributing

Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
