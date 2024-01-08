console.log('Hello World!');

import { readImagesFromDatabase } from "./database.js";
readImagesFromDatabase(function(list){
   
       console.log("list = ", list);
       for (let x = 0; x < list.length; x++) {            
        const element = '<img src="' + list[x] + '">'
        document.querySelector('.images').innerHTML += element;
    }
   });  
   




