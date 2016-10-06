import React, { Component } from 'react';
import './App.css';
import { Navbar, Jumbotron, Button, FormGroup, FormControl, Form, ControlLabel } from 'react-bootstrap';
import $ from 'jquery'

var API_URL = "https://l2eccf6n1c.execute-api.eu-west-1.amazonaws.com/prod"
// Example word. Meta-dictionary.
var sozluk = [
  {
    "updated": "2016-09-23T01:03:14.758821",
    "related_entries": {
      "idioms": [],
      "compound_entries": [
        "sözlük bilgisi",
        "sözlük birimi",
        "ansiklopedik sözlük",
        "cep sözlüğü",
        "el sözlüğü"
      ]
    },
    "created": "2016-09-23T01:03:14.758821",
    "sources": [
      {
        "definitions": [
          {
            "meaning": "Bir dilin bütün veya belli bir çağda kullanılmış kelime ve deyimlerini alfabe sırasına göre alarak tanımlarını yapan, açıklayan, başka dillerdeki karşılıklarını veren eser, lügat",
            "example": {
              "sentence": "Türkçe Sözlük, Tarama Sözlüğü, Fransızca-Türkçe Sözlük, Türkçeden Almancaya Sözlük.",
              "author": null
            },
            "tags": [
              "isim"
            ]
          }
        ],
        "tags": [
          "isim"
        ]
      }
    ],
    "entry": "sözlük",
    "norm": "sozluk"
  }
];


class SearchBar extends Component {
  constructor(props) {
    super(props);
    // bind this. React.createClass apparently does this automatically.
    this.entryChange = this.entryChange.bind(this);
    this.formSubmit = this.formSubmit.bind(this);
  }

  formSubmit(e) {
    e.preventDefault();
    this.props.getEntryList(this.state.entry);
  }

  entryChange(e) {
    this.setState({entry: e.target.value});
  }

  render() {
    return (
        <Navbar componentClass="header">
          <Navbar.Form>
            <Form onSubmit={this.formSubmit} inline>
              <FormGroup>
                <ControlLabel
                  srOnly={true}>
                  Kelime
                </ControlLabel>
                <FormControl
                  name="entry"
                  onChange={this.entryChange}
                  placeholder="sozluk">
                </FormControl>
                {'  '}
                <Button
                  bsStyle="success"
                  type="submit" >
                  Getir
                </Button>
              </FormGroup>
            </Form>
          </Navbar.Form>
        </Navbar>
    );
  }
}

class Definition extends Component {
  render() {
    return (
      <li className="Definition">
        <div className="Definition.Tags">
          {
            this.props.definition.tags.join(', ')
          }
        </div>
        <div className="Meaning">
          {this.props.definition.meaning}
        </div>
        <div className="Example">
          <div className="Sentence">
            {this.props.definition.example.sentence}
          </div>
          <div className="Author">
            {this.props.definition.example.author}
          </div>
        </div>
      </li>
    );
  }
}


class Definitions extends Component {
  render() {
    return (
      <ol className="Definitions">
      {
        this.props.definitions.map(function(definition, i){
          return <Definition key={i} definition={definition} />;
        })
      }
      </ol>
    );
  }
}


class Source extends Component {
  render() {
    return (
      <div className="Source">
        <div className="EntryHeader">
          <div className="Entry.Entry">
            {this.props.entry}
          </div>
          <div className="Source.Tags">
            {
              this.props.source.tags.join(', ')
            }
          </div>
        </div>
        <Definitions definitions={this.props.source.definitions} />
      </div>   
    );
  }
}


class Sources extends Component {
  render() {
    return (
      <div className="Sources">
        {
          this.props.sources.map(function(source, i){
            return <Source key={i} entry={this.props.entry} source={source} />;
          }, this)
        }
      </div>  
    );
  }
}


class Entry extends Component {
  render() {
    return (
      <div className="Entry">
        <Sources sources={this.props.entry.sources} entry={this.props.entry.entry} />
      </div>
    );
  }
}


class EntryList extends Component {
  render() {
    return (
      <div className="EntryList">
        {
          this.props.entry_list.map(function(entry, i){
            return <Entry key={i} entry={entry} />;
          })
        }
      </div>
    );
  }
}


class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      entry_list: sozluk
    };
    this.getEntryList = this.getEntryList.bind(this);
    if (props.entry) {
      this.getEntryList(props.entry);
    }
  }

  getEntryList(entry) {
    window.location.hash = '#' + entry;
    $.ajax({
      url: API_URL,
      dataType: "json",
      data: {entry: entry},
      cache: true,
      success: function(entry_list) {
        // Sort result so we give precedence to exact query.
        entry_list.sort(function(a, b){
          if (a.entry === b.entry) {
            return 0;
          }
          if (a.entry === entry) {
            return -1;
          }
          if (b.entry === entry) {
            return 1;
          }
          return 0;
        });
        this.setState({entry_list: entry_list})
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(status, err.toString());
      }
    });
  }

  render() {
    return (
      <div>
      <Jumbotron className="App">
        <SearchBar getEntryList={this.getEntryList} />
      </Jumbotron>
      <EntryList entry_list={this.state.entry_list} />
      </div>
    );
  }
}


export default App;