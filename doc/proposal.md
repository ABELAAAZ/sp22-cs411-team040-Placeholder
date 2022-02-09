## 1.Project Title
 **Pokémon Trading Card system**
 
## 2.Project Summary 
We want to design a platform that focuses on Pokémon card selling and p2p trading. Our platform can be mainly divided into two functional modules. These two parts are that the platform sells Pokémon card blind boxes to users and users trade Pokémon cards to each other. For the first part, the platform will not sell a specific card but in the form of a blind box. Users who purchase a blind box will randomly get cards within a fixed range of pokemon cards. After getting the card, users can choose to mail the card or resell the card they don't like directly on the website. Or if they want, they can directly buy a single card resold by other users instead of buying the blind boxes sold by the platform.
 
## 3.Description of an application of your choice.
The primary purpose of the proposed project is to create a convenient and powerful platform for users to purchase and trade Pokémon cards. One application is P2P cards trading. Users can check the trading history and historical price of individual cards and use the information of trading trends to decide the posted card's selling price. Then, buyers interested in buying specific cards can inquire about sellers who are selling that card. By comparing the prices between sellers and checking the historical price of that card or similar cards, the buyers can decide whether to buy the card and to buy from which seller.

## 4.Usefulness. 
### Explain as clearly as possible why your chosen application is useful.  Make sure to answer the following questions: Are there any similar websites/applications out there?  If so, what are they, and how is yours different?
Our platform will be useful in terms of three aspects. First, compared to the official Pokémon card selling site, our first functional module offers a more affordable option for users to purchase card packages. By selling used cards, the platform can control the package price at a lower rate. Second, unlike similar websites such as card trader that only allows for P2P cards trading and simple seller inquiry, our second functional module enables users to check the trading history and historical price of individual cards so users can make better decisions on card trading. Third, the effective combination of the first and second modules can create a more smooth and efficient user experience. As mentioned, users can unpack the packages online and resell the cards on the website immediately.

## 5.Realness.  
### Describe what your data is and where you will get it.




## 6.Description of the functionality that your website offers. 

### Describe what data is stored in the database. (Where is the data from, what attributes and information would be stored?)
	First of all, we will collect data sets about Pokémon cards from the Internet. If we can't find enough data, we will directly use the data of Pokémon to make card information data, which includes Pokémon's id, name, type, rarity, description, which box it belongs to, and other attributes. For the blind box, we will refer to the products on the market, including attributes such as id, name, price, number of cards, etc. We will randomly generate customer data, including id, name, account number and password. Other data includes cards owned by customers, purchase history, sales history, and more.
### What are the basic functions of your web application? (What can users of this website do? Which simple and complex features are there?)
	Customers can log on to the website, buy boxes on the website, and open the boxes to get cards randomly. Customers can also view cards on sale and purchase them, or sell cards they own. For boxes and cards that are on sale, we will implement search and sorting functions. And customers can view the information of the box or card. Customers can also view their purchase history, sales history, and owned cards, and retrieve them by conditions.
  
## 7.What would be a good creative component (function) that can improve the functionality of your application? 
### What is something cool that you want to include? How are you planning to achieve it?)
  
Create a function to guess users’ preferences. Also, we would like to design a feature on the resale page to view the trend of the transaction amount of similar products. To achieve those goals, we are going to store the searching history, then classify and guess preferences. For a similar product, we can collect the transaction data, then show the trend or other analysis by using the chart.

## 8.A low fidelity UI mockup:
![avatar](C:\Users\92815\Desktop\uiuc\2022spring\CS411\UI.png)

## 9.Project work distribution: 
### Who would be responsible for each of the tasks or subtasks?

conceptual modeling : 
---Create entities and attributes: Yanying Yu/ Bill Ho Nam Wong.
---add relationship and contraints: Nengyu Wang/ Jiajun Wang.

Database Implementation and Indexing:
---Create TABLE DDL : Nengyu Wang
---Insert DATA：Billhonam Wong
---Develop two advanced SQL queries:Yanying Yu/JiaJun Wang

Midterm-Demo：
--front end application: Nengyu Wang/Yanying Yu
---connect to the database: Jiajun Wang/Bill honam Wong





