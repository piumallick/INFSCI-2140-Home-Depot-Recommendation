/**
 * Created on November 21, 2020
 * @author Aishwarya Jakka
 */
const dotenv = require('dotenv');
var createError = require("http-errors");
var express = require("express");
var session = require("express-session");
var path = require("path");
var cookieParser = require("cookie-parser");
var bodyParser = require("body-parser");
var indexRouter = require("./routes/index");
//var recommendRouter = require("./routes/recommend");
dotenv.config();

var app = express();
const port = process.env.PORT || 5000;

// view engine setup
app.set("views", path.join(__dirname, "views"));
app.set("view engine", "ejs");


app.use(express.static(path.join(__dirname, "public")));
app.use(cookieParser());


app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended:true}));


app.use("/", indexRouter);
//app.use("/recommend", recommendRouter);


app.listen(port, () => console.log(`Example app listening on port ${port}!`))

module.exports = app;
