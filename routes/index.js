/**
 * Created on November 21, 2020
 * @author Aishwarya Jakka
 */
var express = require('express');
var router = express.Router();
var spawn = require("child_process").spawn;

/* GET home page. */
router.get('/', function(request, response, next) {
  response.render('index');
});

/* GET THE STRING amd call Main.py */
router.post("/result", function(request, response) {
  

  const searchText = request.body.searchBar;
  //Sample product json array
  /*var product = [
     {
      product_uid: 1,
      product_title: "Makeup Kit"
    },
   {
      product_uid: 2,
      product_title: "Kylie fancy Kit fancy"
    },
    {
      product_uid: 3,
      product_title: "I am a barbie girl"
    }

  ];*/
  let dataString
  // spawn new child process to call the python script
  const python = spawn('python', ['./scripts/SearchEngine/Main_Copy.py', searchText])

  // collect data from script
  python.stdout.on('data', function (data) {
    console.log('Pipe data from python script ...')
    //dataToSend =  data;
    dataString += data.toString();
  })

  // in close event we are sure that stream is from child process is closed
  python.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`)
    // send data to browser
    
    result = JSON.parse(dataString.slice(9))
    //console.log(dataString)
   return response.render("results",{ value : searchText,products : result});
  })
})
  
 
  

 
  /* GET THE Product title amd call recommend.py */

  router.get('/:title/recommend', function(request, response, next) {
    product_title = request.params.title;
    /*
    var recommend = [
      {
       product_uid: 1,
       product_title: "Makeup Kit"
     },
    {
       product_uid: 2,
       product_title: "Kylie fancy Kit fancy"
     },
     {
       product_uid: 3,
       product_title: "I am a barbie girl"
     }]*/

   // response.json(recommend)
   let dataString
   // spawn new child process to call the python script
   const python = spawn('python', ['./scripts/SearchEngine/Recommendation.py', product_title])
 
   // collect data from script
   python.stdout.on('data', function (data) {
     console.log('Pipe data from python script ...')
     //dataToSend =  data;
     dataString += data.toString();
   })
 
   // in close event we are sure that stream is from child process is closed
   python.on('close', (code) => {
     console.log(`child process close all stdio with code ${code}`)
     // send data to browser
     
     result = JSON.parse(dataString.slice(9))
     //console.log(dataString)
     return response.render("recommend",{ value : product_title ,products : result});
   })


   

  });

module.exports = router;
