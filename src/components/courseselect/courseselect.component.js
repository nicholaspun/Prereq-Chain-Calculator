import React, { Component } from 'react';
import "./courseselect.component.css"; // Styles

export default class CourseSelect extends Component {
  constructor() {
    super();
    this.state = {
      deptOptions: [],
      codeOptions: [],
      prereq: [],
    }

    // Function Binding
    this.changeDept = this.changeDept.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  componentDidMount() {
    fetch(process.env.API_URL + "codes/subjects.json?key=" + process.env.API_KEY)
      .then((res) => res.json())
      .then((json) => {
        const deptOptions = json.data.map((obj) => obj.subject);
        this.setState({ deptOptions: deptOptions });
      })
      .catch((err) => console.log(err))
  }

  errorHandler(err) {
    // This will eventually raise an error saying the course code is incorrect
    console.log(err);
    console.log("An error has occurred");
  }

  formatURL(dept, code) {
    return process.env.API_URL + 'courses/' + dept + "/" + code + "/prerequisites.json?key=" + process.env.API_KEY;
  }

  handleSubmit(event) {
    event.preventDefault();
    const dept = event.target.dept.value;
    const code = event.target.code.value;
    console.log("handleSubmit(): ", dept, code);
    fetch(this.formatURL(dept, code))
      .then((res) => res.json())
      .then((json) => {
        console.log(json.data.prerequisites_parsed);
        this.setState({ prereq: json.data.prerequisites_parsed });
      })
      .catch((err) => this.errorHandler(err))
  }

  changeDept(event) {
    const value = event.target.value;
    fetch(process.env.API_URL + "courses/" + value + ".json?key=" + process.env.API_KEY)
      .then((res) => res.json())
      .then((json) => {
        const codeOptions = json.data.map((obj) => obj.catalog_number);
        this.setState({ codeOptions: codeOptions });
      })
      .catch((err) => console.log(err))
  }

  renderDeptOptions() {
    return this.state.deptOptions.map((option) => {
      return <option value={option} key={option}>{option}</option>
    })
  }

  renderCodeOptions() {
    return this.state.codeOptions.map((option, key) => {
      return <option value={option} key={key}>{option}</option>
    })
  }

  renderPrereq(arr) {
    return (
      <ul>
          {
            arr.map((option) => {
              if (option.constructor === Array) return this.renderPrereq(option)
              else return <li value={option} key={option}>{option}</li>
            })
          }
      </ul>
    )
  }

  render () {
    return (
      <div>
        <form onSubmit={this.handleSubmit}>
          <select name="dept" onChange={this.changeDept}>
            {this.renderDeptOptions()}
          </select>
          <select name="code">
            {this.renderCodeOptions()}
          </select>
          <input type="submit" />
        </form>
        {this.renderPrereq(this.state.prereq)}
      </div>
    )
  }
}
