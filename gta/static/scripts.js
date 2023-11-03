// static/scripts.js

document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        let alerts = document.querySelectorAll('.alert:not(.static-alert)');
        alerts.forEach(function(alert) {
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.style.display = 'none';
            }, 1000); // Matches the duration of the fade effect
        });
    }, 5000); // Duration until the fade-out starts
});


function togglePasswordVisibility() {
    const passwordField = document.getElementById('passwordField');
    const passwordType = passwordField.getAttribute('type');
    
    if (passwordType === 'password') {
        passwordField.setAttribute('type', 'text');
    } else {
        passwordField.setAttribute('type', 'password');
    }
};

function resetJobs()
{
    let coursef = document.getElementById("course-filter");
    let jobgroup = document.getElementById("job-list-group");
    let arr = new Array();
    for(c of jobgroup.children) { arr.push(c); };
    for (a of arr) { a.remove(); };
    "{% for j in jobs%}";
    var item = document.createElement('li');
    item.className = "list-group-item";
    var t = document.createElement('h5');
    t.innerHTML = "{{j[0]}} - {{j[3]}} ";
    var b = document.createElement('span');
    b.className = "badge badge-primary";
    b.innerHTML = "{{j[2]}}";
    t.appendChild(b);
    var pi = document.createElement('p');
    pi.setAttribute("value", "{{j[4]}}");
    pi.innerText = "Course ID: {{j[4]}}"
    pi.id = "job-course-id";
    var pc = document.createElement('p');
    pc.innerHTML = "{% if j[1] == 1 %}*Requires Certification{% else %}&nbsp;{% endif %}";
    var sb = document.createElement('a');
    sb.href = "{{ url_for('form.Apply', job_id=loop.index|string) }}";
    sb.className = "btn apply-btn";
    sb.innerText = "Apply";
    item.appendChild(t);
    item.appendChild(pi);
    item.appendChild(pc);
    item.appendChild(sb);
    jobgroup.appendChild(item);
    "{% endfor %}";
}
function courseChange()
{
    resetJobs();
    let arr = new Array();
    let coursef = document.getElementById("course-filter");
    if (coursef.options[coursef.selectedIndex].value != "")
    {
        let items = document.getElementsByClassName("list-group-item");
        for(var i of items)
        {
            if(i.childNodes[1].attributes.value.value !== coursef.options[coursef.selectedIndex].value)
            {
                arr.push(i);
            }
        }
        for (a of arr) { a.remove() };
    }
};

function certRequired()
{
    //console.log(this);
    var arr = new Array()
    var cur = document.getElementById("cert-filter").checked;
    let items = document.getElementsByClassName("list-group-item");
    if (cur === true)
    {
        for(var i of items)
        {
            if (i.childNodes[2].innerHTML === "&nbsp;")
            {
                arr.push(i)
            }
        }
        for(var a of arr)
        {
            a.remove();
        }
    }
    else
    {
        for(var i of items) { i.remove()};
        "{% for j in jobs %}";

        "{% endfor %}";
    }
}
function roleChange()
{

};
