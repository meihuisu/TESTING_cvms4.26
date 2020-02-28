//
//

// one set per url
var  iPlot_data=[]; // data
var  iPlot_label=[]; // data's label/header
var  iPlot_title=[]; // title for the plot

var  frameWidth=0;
var  frameHeight=0;

var defaultColor=[
                   '#DF013A',
                   '#298A08',
                   '#0174DF',
                   '#FF8000',
                   '#298A08',
                   
                   '#3A848F',
                   '#0469B4',
                   '#8F3A53',
                 ];

/*****MAIN*****/
jQuery(document).ready(function() {

//window.console.log("in Ready call..");

  frameHeight=window.innerHeight;
  frameWidth=window.innerWidth;

  refreshPlot();
}) // end of MAIN

function linesPlot() {
  var configs=[];
  configs.push(stuffConfig(0)); 
  var height=frameHeight * 0.85;
  var width= height * 1.2;
  addLinesPlot("#myDiv", configs, width, height);
}

function refreshPlot()
{
  $('#myDiv').empty();
  iPlot_data=[]; // data
  iPlot_label=[]; // data's label/header
  iPlot_title=[]; // title for the plot

  var url= newUrl();
  var title = loadAndProcessCSVfromFile(url);
  iPlot_title.push(title);
  linesPlot();
}
