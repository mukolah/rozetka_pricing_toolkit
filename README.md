<p align="center">
  <a href="https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fmukolah%2Frozetka_pricing_toolkit.git"><img src="https://vercel.com/button" alt="Deploy with Vercel"/></a>
  <a href="https://github.com/mukolah/rozetka_pricing_toolkit/archive/refs/heads/main.zip"><img src="https://img.shields.io/badge/Download-1e1e1e?logo=python" alt="Download"/></a>
</p>

# Rozetka "Purchase Manager"  
A simple tool to obtain a list of items from rozetka.com.ua based on filtered selection.

Just open rozetka category of your choice, apply filters, copy page URL into the tool and it will get thorugh all pages for you. 

The structure as follows: Name (with clickable link) | Price

You can add additional columns using regex from name.

## Screenshots  

<img align="left" width="422" height="189" src="https://github.com/mukolah/other_storage/blob/main/rztk_1.jpg?raw=true">

- Pull a list  of store items

- Enable / Disable collection of out of stock items

- Sort default columns (name, price) as well as any custom

- Export data as .csv
<br>

---

<img align="right" width="622" height="179" src="https://github.com/mukolah/other_storage/blob/main/rztk_3.jpg?raw=true">

<br>

- Add new columns using any custom regex based on product name in the list
<br>
<br>

---

<p align="center">
  Build price heatmap to find best value product 
<br>
<br>
  <img width="100%" src="https://github.com/mukolah/other_storage/blob/main/rztk_4.jpg?raw=true">
</p>

---

## Run Locally  

Clone the project  

```
git clone https://github.com/mukolah/rozetka_pricing_toolkit.git
```

Go to the project directory  

```
cd rozetka_pricing_toolkit
```

Install dependencies  

```
pip install -r requirements.txt
```

Start the server  

```
py rozetka.py
```

Connect to the local server 

http://127.0.0.1:5000

## Run in Cloud  

 - Paid: deploy instantly to any python powered cloud solutions using git.
 - Free: use deploy button above to run app in Vercel.
