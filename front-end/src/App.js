import React, { Component } from 'react';
import { Navbar, Button, FormGroup, FormControl, Form, ControlLabel, Modal } from 'react-bootstrap';
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
    this.state = {
      entry: this.props.entry
    }
  }

  formSubmit(e) {
    e.preventDefault();
    var entry = this.state.entry;
    history.pushState({entry: entry}, entry + " anlami", '/sozluk/#' + encodeURIComponent(entry))
    this.props.getEntryList(entry);
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
                  type="text"
                  name="entry"
                  required={true}
                  autoCapitalize="none"
                  onChange={this.entryChange}
                  value={this.state.entry}
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
    var blockquote = ''
    var footer = ''
    if (this.props.definition.example.author) {
      footer = <footer className="Author blockquote-footer">
                  {this.props.definition.example.author}
               </footer>
    }
    if (this.props.definition.example.sentence) {
      blockquote = <div><blockquote className="Example">
                    <p className="Sentence">
                      {this.props.definition.example.sentence}
                    </p>
                    {footer}
      </blockquote>
      </div>
    }
    return (
      <li className="Definition">
        <div className="DefinitionTags">
          {
            this.props.definition.tags.join(', ')
          }
        </div>
        <div className="Meaning">
          {this.props.definition.meaning}
        </div>
        {blockquote}
      </li>
    );
  }
}


class Definitions extends Component {
  render() {
    return (
      <ol className="Definitions col-sm-8">
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
      <div className="Source row">
        <div className="EntryHeader col-sm-4">
          <div className="EntryKeyword">
            {this.props.entry}
          </div>
          <div className="SourceTags">
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


class ExtraInfo extends Component {
  render() {
    if (!this.props.entries.length) {
      return null;
    }
    this.props.entries.sort();
    return (
      <div className="ExtraInfo">
        <div className="col-sm-4 ExtraInfoTitle">{this.props.title}</div>
        <div className="col-sm-8">
          <div className={this.props.name}>
          {
            this.props.entries.map(function(entry, i) {
              return <a key={i} href={"/sozluk/#" + encodeURIComponent(entry)}>{entry}</a>;
            }, this)
          }
          </div>
        </div>
      </div>
    )
  }
}


class Entry extends Component {
  render() {
    return (
      <div className="Entry">
        <Sources sources={this.props.entry.sources} entry={this.props.entry.entry} />
        <ExtraInfo name="idioms" entries={this.props.entry.related_entries.idioms} title="Deyimler" />
        <ExtraInfo name="compound_entries" entries={this.props.entry.related_entries.compound_entries} title="Birleşik Kelimeler" />
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


class MessageModal extends Component {
  render() {
    return (
      <Modal show={this.props.show} bsSize="small" aria-labelledby="contained-modal-title-sm" onHide={this.props.onHide}>
        <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-sm">{this.props.title}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {this.props.text}
        </Modal.Body>
        <Modal.Footer>
          <Button onClick={this.props.onHide}>Kapat</Button>
        </Modal.Footer>
      </Modal>
    );
  }
}


class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      entry: '',
      entry_list: sozluk,
      show_modal: false,
      message: {
        title: 'Hata',
        text: 'Hata',
      }
    };
    this.getEntryList = this.getEntryList.bind(this);
  }

  getEntryList(entry) {
    // push new state.
    if (!entry) {
      entry = this.state.entry;
    } else {
      this.setState({entry: entry});
    }
    $("#loading").show();
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
        this.setState({entry_list: entry_list});
        $("#loading").hide();
      }.bind(this),
      error: function(xhr, status, err) {
        if (xhr.status === 404) {
          this.setState({
            show_modal: true,
            message: {
              title: 'Kelime bulunamadı',
              text: <h5><b>{entry}</b> kelimesi veritabanında bulunamadı.</h5>,
            }
          })
        } else {
          this.setState({
            show_modal: true,
            message: {
              title: status,
              text: <h5>{err.toString()}</h5>,
            }
          })
        }
        $("#loading").hide();
      }.bind(this)
    });
  }

  render() {
    let modalClose = () => this.setState({show_modal: false});
    return (
      <div className="App">
        <SearchBar getEntryList={this.getEntryList} entry={this.state.entry} />
        <EntryList entry_list={this.state.entry_list} />
        <MessageModal
          show={this.state.show_modal}
          title={this.state.message.title}
          text={this.state.message.text}
          onHide={modalClose} />
      </div>
    );
  }
}


export default App;
