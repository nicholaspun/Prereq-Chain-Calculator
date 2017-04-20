import React, { Component } from 'react';
import './app.css';

import CourseSelect from './components/courseselect/courseselect.component';
// import CourseTree from './components/coursetree/coursetree.component';

export default class App extends Component {
  render () {
    return (
      <div style={{ textAlign: "center"}}>
        <CourseSelect></CourseSelect>
      </div>
    )
  }
}
