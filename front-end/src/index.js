import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';
import './index.css';

var react_obj = null;


function handlePage(event) {
  var location = window.location.hash.replace(/^#\/?|\/$/g, '').split('/');
  var entry = decodeURIComponent(location[0]);
  if (!react_obj) {
    react_obj = ReactDOM.render(
        <App />,
        document.getElementById('root')
    );
  }
  if (entry) {
    react_obj.getEntryList(entry);
  }
}

// Handle the initial route and browser navigation events
handlePage()
window.addEventListener('popstate', handlePage, false);
