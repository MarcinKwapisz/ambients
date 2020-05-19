function view(param)
{
    var str = param.split('v=')[1]
    str = str.split('&')[0]
    var div = document.createElement('iframe');
    str = 'https://www.youtube.com/embed/'+str
div.setAttribute('class', 'video');
div.setAttribute('width', '560');
div.setAttribute('height', '315');
div.setAttribute('src', str);
div.setAttribute('frameborder', '0');
div.setAttribute('allow', 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture');
document.body.appendChild(div);
}
$(document).mouseup(function(e)
{
    var container = $(".video");

    // if the target of the click isn't the container nor a descendant of the container
    if (!container.is(e.target) && container.has(e.target).length === 0)
    {
        container.remove();
    }
});