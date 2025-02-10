import {useState} from "react";

function UserRegistration() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        if (!username || !password) {
            alert("Username and password are required fields.")
            return;
        }

        const userData = {username, password};

        try {
            const response = await fetch("http://localhost:5000/register", {
                 method: "POST",
                 headers: {"Content-Type": "application/json"},
                 body: JSON.stringify(userData),
                })
               

          
            if (response.ok) {
                alert("User registered successfully!");
            } else {
                const result = await response.json();
                alert(result.error || "Error occurred");
            }

    }

            catch (error) {
                alert("Failed to register the user.");
                console.error(error);
            }

};

            return (
                <div>
                    <h1>User Registration Form</h1>
                    <form onSubmit={handleSubmit}>
                        <div>
                            <label htmlFor="username">Username:</label>
                            <input type="text" id="username" value={username} onChange={(e) => setUsername(e.target.value)}></input>
                        </div>
                        <div>
                            <label htmlFor="password">Password:</label>
                            <input type="password" id="password" value={password} onChange={(e) => setPassword(e.target.value)}></input>
                        </div>
                        <button type="submit">Click Here To Register</button>
                    </form>
                </div>
            )
        }