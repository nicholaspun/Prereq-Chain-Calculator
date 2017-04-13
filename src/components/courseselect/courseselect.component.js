import React, { Component } from 'react';
import "./courseselect.component.css"; // Styles

export default class CourseSelect extends Component {
  constructor() {
    super();
    this.state = {
      deptOptions: [],
      codeOptions: [],
      dept: "",
      code: ""
    }

    // Function Binding
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  componentDidMount() {
    fetch("https://api.uwaterloo.ca/v2/codes/subjects.json?key=06433ec8e376706dcc588a055f983fc7")
      .then((res) => res.json())
      .then((json) => {
        const deptOptions = json.data.map((obj) => obj.subject);
        this.setState({ deptOptions: deptOptions });
      })
      .catch((err) => console.log(err))
  }

  errorHandler() {
    // This will eventually raise an error saying the course code is incorrect
    console.log("An error has occurred");
  }

  getPrereqs(url) {
    fetch(url)
        .then((res) => res.json())
        .then((json) => {
          console.log(json)
        })
        .catch((err) => this.errorHandler())
  }


  formatURL(dept, code) {
    const key = "06433ec8e376706dcc588a055f983fc7";
    return process.env.API_URL + 'courses/' + dept + "/" + code + "/prerequisites.json?key=" + key;
  }

  handleSubmit(event) {
    event.preventDefault();
    console.log("handleSubmit(): ", this.state.dept, this.state.code);
    const url = this.formatURL(this.state.dept, this.state.code);
    this.getPrereqs(url)
  }

  handleChange(event) {
    const value = event.target.value;
    const name = event.target.name;
    this.setState({ [name]: value });
    if (name == "dept") {
      fetch("https://api.uwaterloo.ca/v2/courses/" + value + ".json?key=06433ec8e376706dcc588a055f983fc7")
        .then((res) => res.json())
        .then((json) => {
          const codeOptions = json.data.map((obj) => obj.catalog_number);
          this.setState({ codeOptions: codeOptions });
        })
        .catch((err) => console.log(err))
    }
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

  render () {
    return (
      <div>
        <form onSubmit={this.handleSubmit}>
          <select name="dept"
                  onChange={this.handleChange}>
            {this.renderDeptOptions()}
          </select>
          <select name="code"
                  onChange={this.handleChange}>
            {this.renderCodeOptions()}
          </select>
          <input type="submit" />
        </form>
      </div>
    )
  }
}
