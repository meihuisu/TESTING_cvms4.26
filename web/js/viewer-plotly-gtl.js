function newUrl() {
  var datagroup=document.getElementById("dataGroup").value;
  var datatype=document.getElementById("dataType").value;

  var newurl= "data/"+datagroup+"_GTL_all_"+datatype+".csv";
  return newurl;
}


/*
https://stackoverflow.com/questions/45104632/plotly-js-modebar-download-as-png-give-png-a-name
*/
/**************************************************************/
function addAPlot(data, layout, image_fname) {
//  var nplot=Plotly.newPlot('myDiv', data, layout, {displayModeBar: false});
  var nplot=Plotly.newPlot('myDiv', data, layout,
        {
           toImageButtonOptions: {
              filename: image_fname,
              format: 'png'
           }
        });
  return nplot;
}

/**************************************************************/
//each config=[pdata,title,label]
function addLinesPlot(divname, configs, fwidth, fheight) {
  var pcnt=configs.length; //
  if(pcnt < 1) 
    return;
  var config=configs[0];
  var pdata=config[0];  // array of a single data
  var title=config[1];
  var label=config[2];

  var ctrace=makeCompareDataTraces(pdata,'UCVM-25 & BILLY-25',1,0,6);
  var mdata=makeLinesDataTraces(pdata,label);
  var _data=mdata.concat(ctrace);

  var _layout=getPlotlyLayout(fwidth, fheight,"Vs (m/s)","Depth(m)",title);
  var _width=fwidth;
  var _height=fheight;

  if(fwidth > 400)
    addAPlot(_data, _layout, title);
    else
      addAPlot(_data, _layout, title);
} 

function makeLinesDataTraces(sdata,label) {
  var sz=sdata.length;
  var ret=[];

  for(var idx=0; idx<sz; idx++) {
    var xval=sdata[idx];
    var ycnt=xval.length;
    var yval=[];
    for( var i=0; i< ycnt; i++) {
       yval.push(i*500);
    }
  
    var marker_val = { 
        size:3,
        symbol:'circle', 
        color: defaultColor[idx], 
        opacity: 1,
        line: {color: 'grey', width: 1}
      };

    var t={ x:xval,
        y:yval,
        name:label[idx],
        marker: marker_val, 
        line: {width:3, opacity:1},
//        mode: "lines+markers",
        mode: "lines",
        type:"scatter" };

   if(idx==0) {
       t.line.width=3;
       t.line.opacity=1;
   }

    ret.push(t);  
  }

  return ret;
}

function getPlotlyLayout(w,h,xaxis,yaxis,title) {
  var datatype=document.getElementById("dataType").value;
  var p= {
        xaxis: {
          domain: [0, 0.7],
          title: xaxis,
          showline: true,
          ticks:'outside',
          linewidth: 2,
//          range: [0,5000], // 0, 5000(km/s)
          zeroline: true
        },
        yaxis: {
          title: yaxis,
          showline: true,
          ticks:'outside',
          linewidth: 2,
          range: [50000,0],  // 0, 50km
          zeroline: true
        },
        width: w,
        height: h,
        margin: { t:50, b:40 },
        showlegend: true,
        hovermode: 'closest',
        legend: { traceorder: 'reversed' },
// closeness scatter plot
  yaxis2: {
    showline: true,
    anchor: 'x2',
    range: [50000,0],  // 0, 50km
    zeroline: true
  },
  xaxis2: {
    showline: true,
    domain: [0.8, 1],
    zeroline: true,
    title: 'Closeness'
  },
        };

  if(datatype == "vs") {
   p.xaxis.range=[0,5000];
  }

  if(title != null) {
    p.title=title;
  }
  return p;
}

/**************************************************************/

function makeCompareDataTraces(sdata,label,with1, base2, cidx) {
  var sz=sdata.length;

  var xval1=sdata[with1];
  var xval2=sdata[base2];
  var sz=xval1.length;
  var absdiff=[];
  var percentdiff=[];
  var percentdiff2=[];
  var ycnt=xval1.length;
  var yval=[];
  for( var i=0; i< ycnt; i++) {
       yval.push(i*500);
  }
  for(var i=0; i< sz; i++) {
    var adiff=Math.abs(xval1[i]-xval2[i]);
    absdiff.push( adiff );
    var pdiff= adiff/(xval2[i]) * 100;
    percentdiff.push(pdiff);
    var pdiff2= adiff/((xval1[i]+xval2[i])/2) * 100;
    percentdiff2.push(pdiff2);
  }

  var t = { 
           x: percentdiff,
           y: yval,
           name:label,
           type: 'scatter',
           mode: "lines+markers",
           marker: {color: defaultColor[cidx]}, 
           line: {width:1, opacity:1},
           xaxis: 'x2',
           yaxis: 'y2'
         };

  return [t];
}
