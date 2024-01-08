console.log('Hello World!');

export function readImagesFromDatabase(callback){
const sqlite3 = require('sqlite3').verbose();
//import sqlite3;
let db = new sqlite3.Database('C:/Users/potyaga2/Documents/Custom/python_scripts/project/rasa_store.db', (err) => {
          if (err) {
            console.error(err.message);
          }
          console.log('Connected to the chinook database.');
         
                  
        });
images_list = []
db.serialize(() => {
  
  
  db.each(`SELECT data FROM 'events' WHERE data LIKE "%found%"`, (err, row) => {
    if (err) {
      console.error(err.message);
    }
    myJSON = JSON.stringify(row);
    //console.log(row);
    let left = myJSON.indexOf("[");
    let right = myJSON.indexOf("]");
    //console.log(myJSON);
    //console.log(left);
    //console.log(right);
    substring = myJSON.slice(left+1, right-1);
    images_list = substring.split(',');
    console.log(images_list[0].slice(1,-1));
    images_list[0] = "https://drive.google.com/drive/u/0/folders/1QUSwQ6_l6ho6HKnPc77r7zxlFlQG8DL8/" + images_list[0].slice(1,-1) + ".jpg";
    for (let x = 1; x < images_list.length; x++) {            
       images_list[x] = "https://drive.google.com/drive/u/0/folders/1QUSwQ6_l6ho6HKnPc77r7zxlFlQG8DL8/" + images_list[x].slice(2,-1) + ".jpg";
       
    }
        //console.log(images_list);
        callback(images_list);
      });


    });

    }


readImagesFromDatabase(function(list){
   
       console.log("list = ", list);
       for (let x = 0; x < list.length; x++) {            
        const element = '<img src="' + list[x] + '">'
        document.querySelector('.images').innerHTML += element;
    }
   });  
  


