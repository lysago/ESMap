# ESMap

Create a map of epidemiological survey.

***

## __1. Input__

### __1.1 Excel__

> 3 sheets  
> + **city**  
>   >  Must include **Province** and **City**  
>   > Following Full adress should't include the city again.  
> + **dict**
>   > **Abbreviation** of home or company or school or other >**frequently visited place**  
>   > **2 columes** :
>   > + **key** &emsp; Abbreviation  
>   > + **value** &emsp; Full address  
>* **timeline**
>   > **5 columes** :
>   > + **time**&emsp; &emsp; &emsp;A point-of-time  
>   > + **address**&emsp; &emsp;Full address, should be found in a map  
>   > + **transport**&emsp; Car or Public transportation  
>   > + **content**&emsp; &emsp;Event  
>   > + **remarks**&emsp; &emsp;Epidemic information  
    
### __1.2 Terminal__  

> (now shelving)

## __2. Run__

### __2.1 Environment__

> python 3.8.1    ( Just fit the packets )

### __2.2 Run__

> **`python main.py`**  
> **input "1"** &emsp;*(choose the excel way to read data)*  
> choose the **file "test.xlsx"**
