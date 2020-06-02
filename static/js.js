function show(id)
{
  var x = document.getElementById(id);
  if (x.type === "password")
  {
    x.type = "text";
  }
  else
      {
    x.type = "password";
  }
}

function searchbox() {
    console.log(1)
    var modal = document.getElementById("search");
    modal.style.display = "inline";
}
function searchboxclose() {
    console.log(1)
    var modal = document.getElementById("search");
    modal.style.display = "none";
}


function view(param)
{
    var t = (param.split('t=')[1])
    if (typeof t === 'undefined')
    {
        t=''
    }
    else
    {
        t='?start='+t.slice(0,-1);
    }
    var str = param.split('v=')[1]
    str = str.split('&')[0]
    var div = document.createElement('iframe');
    str = 'https://www.youtube.com/embed/'+str+t
div.setAttribute('class', 'video');
div.setAttribute('width', '560');
div.setAttribute('height', '315');
div.setAttribute('src', str);
div.setAttribute('frameborder', '0');
div.setAttribute('allow', 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture');
document.body.appendChild(div);
}

setTimeout(function() {
    var container = $(".messages");
    container.remove()
}, 6000);

$(document).mouseup(function(e)
{
    var container = $(".video");

    // if the target of the click isn't the container nor a descendant of the container
    if (!container.is(e.target) && container.has(e.target).length === 0)
    {
        container.remove();
    }
});
