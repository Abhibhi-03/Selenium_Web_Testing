var homes = [];
var index=0;
var numHomes=5;
var images = ["images/5906ChurchillMeadows.PNG", "images/3956Beacham.PNG", "images/1540Elite.PNG", "images/3761Trelawny.PNG", "images/50-7430Copenhagen.PNG"];
var taxes = [4750, 5400, 20000, 6600, 3200];

function CreateHomes() {
    for(var i=0; i<numHomes; ++i) {
        homes[i] = new Home(images[i], taxes[i]);
    }
    var btn = document.querySelector('#submit');
    btn.addEventListener('click', function(e) {
        var username = "<b>"+document.querySelector(".username").value+"</b>";
        var content = document.querySelector(".comment").value;
        homes[index].blogs[homes[index].numBlogs] = username+": "+content;
        ++homes[index].numBlogs;
        RemoveComment();
        DisplayHome();
    });
    DisplayHome();
}

function Home(desc,tax) {
    this.desc = desc;
    this.tax = tax;
    this.value = this.GetValue();
    this.blogs = [];
    this.numBlogs = 0;
}

Home.prototype.GetValue = function() {
    var val = this.tax * 190.00;
    return val.toFixed(2);
}

function Prev() {
    RemoveComment();
    --index;
    if(index<0) {
        index = numHomes-1;
    }
    DisplayHome();
}

function Next() {
    RemoveComment();
    index++;
    if(index>=numHomes) {
        index = 0;
    }
    DisplayHome();
}

function RemoveComment() {
    document.querySelector('.username').value="";
    document.querySelector('.comment').value="";
}

function DisplayHome() {
    document.querySelector("#picture").src = homes[index].desc;
    document.querySelector("#value").innerHTML = "This home should be worth "+homes[index].value;
    var submit = document.querySelector("#submit");
    var div = document.querySelector("#blogs");
    var blogs="";
    for(var i=0; i<homes[index].numBlogs; ++i) {
        blogs+="<p>"+homes[index].blogs[i]+"</p>";
        console.log(blogs);
    }
    div.innerHTML = blogs;
}