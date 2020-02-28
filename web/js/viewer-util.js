function stuffConfig(idx) {
   var pdata=iPlot_data[idx];
   var title=iPlot_title[idx];
   var label=iPlot_label[idx];
   return [pdata,title,label]
}

function getDefaultColor(p) {
  var len=defaultColor.length;
  var t= (p+len) % len;
  return defaultColor[t];
}


// columns> billy, ascii(25), ucvm(25), ascii(0), ucvm(0)
function loadAndProcessCSVfromFile(url) {

  window.console.log("Looking at ",url);
  iplot_data=[];
  iplot_label=[];

  var csv=ckExist(url);
  var csvarray=csv.split('\n');
  var fline=csvarray[0];

// retrieve csv header
  $.csv.toArray(fline, {}, function(err, data) {
      for(var j=0;j<data.length;j++) {
          iplot_label.push(data[j]);
          iplot_data.push([]);
      }
  });


  var sz=csvarray.length;

// retrieve data
  $.csv.toArrays(csv, {}, function(err, data) {
      if(data.length == 0) {
          window.console.log("Fail: can not access ",url);
          exit(1);
      }

      var tmp=data.length;
      var d;
      // skip the header part
      for(var k=1; k<tmp; k++) {
         d=data[k];
         var ttmp=d.length;
         for(var i=0; i<ttmp; i++) {       
           iplot_data[i].push(parseFloat(d[i]));
         }
      }
  });

  iPlot_data.push(iplot_data);
  iPlot_label.push(iplot_label);

  return chopForStub(url);
}

// should be a very small file and used for testing and so can ignore
// >>Synchronous XMLHttpRequest on the main thread is deprecated
// >>because of its detrimental effects to the end user's experience.
function ckExist(url) {
  var http = new XMLHttpRequest();
  http.onreadystatechange = function () {
    if (this.readyState == 4) {
 // okay
    }
  }
  http.open("GET", url, false);
  http.send();
  if(http.status !== 404) {
    return http.responseText;
    } else {
      return null;
  }
};


function chopForStub(url){
  var s=url.split('/').pop();
  var ss=s.slice(0, -4);
  return ss;
}
