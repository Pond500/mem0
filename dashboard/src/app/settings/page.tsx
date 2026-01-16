"use client";
export default function SettingsPage() {
    return (
        <div style={{ maxWidth: "600px" }}>
            <h1 style={{ fontSize: "2rem", fontWeight: "bold", marginBottom: "2rem" }}>Settings</h1>

            <div className="glass-card" style={{ padding: "2rem", borderRadius: "12px" }}>
                <h2 style={{ fontSize: "1.25rem", fontWeight: "600", marginBottom: "1.5rem" }}>Connection</h2>

                <div style={{ marginBottom: "1.5rem" }}>
                    <label style={{ display: "block", marginBottom: "0.5rem", fontSize: "0.9rem", color: "#a1a1aa" }}>
                        API Base URL
                    </label>
                    <input
                        type="text"
                        value="http://localhost:8000"
                        disabled
                        style={{
                            width: "100%",
                            padding: "0.75rem",
                            borderRadius: "8px",
                            background: "rgba(0,0,0,0.2)",
                            border: "1px solid rgba(255,255,255,0.1)",
                            color: "#fff"
                        }}
                    />
                    <p style={{ fontSize: "0.8rem", color: "#666", marginTop: "0.5rem" }}>
                        Currently hardcoded to localhost:8000 for this demo.
                    </p>
                </div>

                <div style={{ padding: "1rem", background: "rgba(16, 185, 129, 0.1)", borderRadius: "8px", border: "1px solid rgba(16, 185, 129, 0.2)", color: "#10b981", fontSize: "0.9rem" }}>
                    ✓ Connected to Local Mem0 API
                </div>
            </div>
        </div>
    );
}
