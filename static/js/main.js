// Nivaldo: "JIRAUSER30619"

function element(element_id) {
    return document.getElementById(element_id)
}

function edit_data(model, id, field, dtype) {

        fetch("/safe/edit/" + model + "/" + id, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            "model": model, "id": id, "key": field, "dtype": dtype, "value": element(field+"|"+id).value
          }),
        })
        .then(response => response.json())
        .then(data => {
          return console.log('Success:', data);
        }).then(
          element("responses").innerHTML = "<b>" + field + "</b> was updated successfully [" + id + "]"
        )
        .catch((error) => {
          console.error('Error:', error);
        });

    }

function edit_role(id) {

        var el_id = "role|"+id
        var role_select_field = element(el_id)

        var selected_role_value = role_select_field.options[role_select_field.selectedIndex].text;
        var selected_role_id = role_select_field.options[role_select_field.selectedIndex].value;

        var values = {"values": [
            {"model": "calendar_event", "id": id, "key": "tempo_role_id", "dtype": "str", "value": selected_role_id},
            {"model": "calendar_event", "id": id, "key": "tempo_role_value", "dtype": "str", "value": selected_role_value}
        ]}

        fetch("/safe/edit/calendar_event/" + id, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(values),
        })
        .then(response => response.json())
        .then(data => {
          return console.log('Success:', data);
        }).then(
          element("responses").innerHTML = "done"
        )
        .catch((error) => {
          console.error('Error:', error);
        });

    }

function trigger_feed_database() {

        var start_date = element("start_date_feed")
        var end_date = element("end_date_feed")

        var values = {
            "start_date": start_date.value,
            "end_date": end_date.value
        }

        var message = "<div style='margin-left: 15px; font-size: 14px;'>Gathering information... Once you see this screen again, reload it.</div>"
        element("app").innerHTML = message;

        fetch("/feed_database", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(values),
        })
        .then(response => response.json())
        .then(data => {
           document.location.reload()
        })
}


function create_alias() {

    var key = element("alias_key")
    var value = element("alias_value")

    var values = {
        "match": key.value,
        "issue_key": value.value
    }

    if (key.value != "")  {

            key.value = ""
            value.value = ""

            fetch("/create_alias", {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(values),
            })
            .then(response => response.json())
            .then(data => {
               document.location.reload()
            })
        }
    }

function add_initiative() {

    var issue_key = element("initiative_issue_key")

    var values = {
        "issue_key": issue_key.value
    }

    if (issue_key.value != "")  {

            issue_key.value = ""

            fetch("/add_initiative", {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(values),
            })
            .then(response => response.json())
            .then(data => {
               document.location.reload()
            })
        }
    }

function show_epics(id) {

    var acc = "epics_" + id
    var div = element(acc)

    if (div.style.display == "none") {
        div.style.display = "block";
        this.innerHTML = "Hide Epics"
    } else {
        div.style.display = "none"
        this.innerHTML = "Show Epics"
    }


}

function confirm_click(next_url, message) {

  if (confirm(message) == true) {
    window.location.replace(next_url)
  }

}