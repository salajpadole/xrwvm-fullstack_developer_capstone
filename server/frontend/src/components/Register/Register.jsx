import React, { useState } from "react";
import Header from "../Header/Header";

const Register = () => {
  const [form, setForm] = useState({ userName: "", firstName: "", lastName: "", email: "", password: "" });
  const [message, setMessage] = useState("");
  const update = (e) => setForm({ ...form, [e.target.name]: e.target.value });
  const submit = async (e) => {
    e.preventDefault();
    setMessage("Submitting registration…");
    try {
      const response = await fetch("/djangoapp/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form)
      });
      const data = await response.json();
      setMessage(response.ok ? (data.message || "Registration request completed.") : (data.message || "Registration failed. Check the server response."));
    } catch (error) {
      setMessage("Could not reach the registration service. Confirm that Django is running.");
    }
  };
  const inputStyle = { display: "block", width: "100%", padding: "12px", margin: "8px 0 16px", border: "1px solid #cbd5e1", borderRadius: "8px" };
  return <div><Header /><main style={{ maxWidth: 480, margin: "40px auto", padding: 24, background: "#fff", borderRadius: 12, boxShadow: "0 8px 24px #0001" }}>
    <h2>Create an account</h2><form onSubmit={submit}>
      <label>Username<input style={inputStyle} name="userName" value={form.userName} onChange={update} required /></label>
      <label>First Name<input style={inputStyle} name="firstName" value={form.firstName} onChange={update} required /></label>
      <label>Last Name<input style={inputStyle} name="lastName" value={form.lastName} onChange={update} required /></label>
      <label>Email<input style={inputStyle} type="email" name="email" value={form.email} onChange={update} required /></label>
      <label>Password<input style={inputStyle} type="password" name="password" value={form.password} onChange={update} required minLength={8} /></label>
      <button type="submit" style={{ padding: "12px 22px", border: 0, borderRadius: 8, background: "#087e8b", color: "white", cursor: "pointer" }}>Register</button>
    </form><p role="status">{message}</p><p>Already registered? <a href="/login">Log in</a></p>
  </main></div>;
};
export default Register;
