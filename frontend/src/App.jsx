import { useState } from "react";

const sampleResults = {
  SQLInjection: {
    title: "SQL Injection",
    cwe: "CWE-89",
    risk: 87,
    confidence: 91,
    test: "SQL Injection PoV",
    status: "Vulnerability Detected",
    features: [
      "SQL query construction",
      "User-controlled input",
      "Database execution"
    ]
  },

  CommandInjection: {
    title: "Command Injection",
    cwe: "CWE-78",
    risk: 92,
    confidence: 94,
    test: "Command Injection PoV",
    status: "Vulnerability Detected",
    features: [
      "Runtime command execution",
      "External input",
      "Process creation"
    ]
  },

  PathTraversal: {
    title: "Path Traversal",
    cwe: "CWE-22",
    risk: 84,
    confidence: 89,
    test: "Path Traversal PoV",
    status: "Vulnerability Detected",
    features: [
      "File path construction",
      "File input operation",
      "Missing path validation"
    ]
  },

  Deserialization: {
    title: "Unsafe Deserialization",
    cwe: "CWE-502",
    risk: 90,
    confidence: 93,
    test: "Deserialization Security PoV",
    status: "Vulnerability Detected",
    features: [
      "ObjectInputStream",
      "readObject()",
      "Untrusted serialized data"
    ]
  },

  AccessControl: {
    title: "Broken Access Control",
    cwe: "CWE-284",
    risk: 78,
    confidence: 86,
    test: "Access-Control Validation PoV",
    status: "Potential Vulnerability",
    features: [
      "Authorization check",
      "Sensitive resource",
      "User-controlled identity"
    ]
  }
};

const sampleFiles = [
  ["Sample_SQLInjection.java", "SQLInjection"],
  ["Sample_CommandInjection.java", "CommandInjection"],
  ["Sample_PathTraversal.java", "PathTraversal"],
  ["Sample_Deserialization.java", "Deserialization"],
  ["Sample_AccessControl.java", "AccessControl"]
];

function App() {
  const [file, setFile] = useState(null);
  const [sample, setSample] = useState("SQLInjection");
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState(null);

  const analyze = () => {
    setAnalyzing(true);
    setResult(null);

    setTimeout(() => {
      setResult(sampleResults[sample]);
      setAnalyzing(false);
    }, 1200);
  };

  const selectSample = (key) => {
    const entry = sampleFiles.find(([, value]) => value === key);

    setSample(key);
    setFile(
      entry
        ? {
            name: entry[0]
          }
        : null
    );

    setResult(null);
  };

  return (
    <div className="app">

      {/* NAVBAR */}

      <header className="navbar">

        <div className="brand">

          <div className="brand-icon">
            N
          </div>

          <div>
            <div className="brand-name">
              NeuroFuzzy Security
            </div>

            <div className="brand-sub">
              Automated Security Patch Validation
            </div>
          </div>

        </div>

        <div className="phase-pill">
          PHASE 1 · VULNERABILITY DETECTION
        </div>

      </header>


      <main className="container">

        {/* HERO */}

        <section className="hero">

          <div>

            <div className="eyebrow">
              AI-POWERED SECURITY ANALYSIS
            </div>

            <h1>
              Neuro-Fuzzy Vulnerability Detection
            </h1>

            <p>
              Upload a Java project and identify potential
              vulnerabilities, calculate risk, and generate
              a security test using the Neuro-Fuzzy framework.
            </p>

          </div>


          <div className="status-card">

            <span className="pulse"></span>

            SYSTEM READY

            <strong>
              Phase 1
            </strong>

          </div>

        </section>


        {/* STATISTICS */}

        <section className="stats">

          <div className="stat">
            <span>DATASET</span>
            <strong>1,056</strong>
            <small>training samples</small>
          </div>

          <div className="stat">
            <span>FEATURES</span>
            <strong>11</strong>
            <small>security features</small>
          </div>

          <div className="stat">
            <span>CLASSES</span>
            <strong>5</strong>
            <small>vulnerability types</small>
          </div>

          <div className="stat">
            <span>ENGINE</span>
            <strong>ANFIS</strong>
            <small>neuro-fuzzy analysis</small>
          </div>

        </section>


        {/* WORKSPACE */}

        <section className="workspace">


          {/* UPLOAD */}

          <div className="panel upload-panel">

            <div className="panel-title">

              <div>

                <span className="step">
                  01
                </span>

                <h2>
                  Upload Java Project
                </h2>

              </div>

              <span className="tag">
                SOURCE INPUT
              </span>

            </div>


            <label className="dropzone">

              <input
                type="file"
                accept=".java,.zip"
                onChange={(e) => {

                  const selected =
                    e.target.files?.[0];

                  if (selected) {

                    setFile(selected);
                    setResult(null);

                  }

                }}
              />

              <div className="upload-icon">
                ↑
              </div>

              <strong>
                {file
                  ? file.name
                  : "Choose a Java file or ZIP project"}
              </strong>

              <span>
                Java source code · ZIP project
              </span>

            </label>


            {/* SAMPLE SELECTOR */}

            <div className="sample-box">

              <label>
                DEMO SAMPLE
              </label>

              <select
                value={sample}
                onChange={(e) =>
                  selectSample(e.target.value)
                }
              >

                {sampleFiles.map(
                  ([name, key]) => (

                    <option
                      key={key}
                      value={key}
                    >
                      {name}
                    </option>

                  )
                )}

              </select>

              <small>
                Five prepared vulnerable Java
                samples are available for demonstration.
              </small>

            </div>


            {/* ANALYZE BUTTON */}

            <button
              className="analyze-btn"
              onClick={analyze}
              disabled={analyzing}
            >

              {analyzing
                ? "ANALYZING SOURCE..."
                : "START PHASE 1 ANALYSIS →"}

            </button>

          </div>


          {/* PIPELINE */}

          <div className="panel pipeline-panel">

            <div className="panel-title">

              <div>

                <span className="step">
                  02
                </span>

                <h2>
                  Analysis Pipeline
                </h2>

              </div>

              <span className="tag">
                LIVE
              </span>

            </div>


            <div className="pipeline">

              {[
                [
                  "01",
                  "Source Analysis",
                  "Java source inspection"
                ],

                [
                  "02",
                  "Vulnerability Detection",
                  "Security pattern analysis"
                ],

                [
                  "03",
                  "Neuro-Fuzzy Analysis",
                  "Risk & confidence"
                ],

                [
                  "04",
                  "Security Test",
                  "PoV generation"
                ]

              ].map(
                ([number, title, description]) => (

                  <div
                    className={`pipeline-row ${
                      analyzing || result
                        ? "active"
                        : ""
                    }`}
                    key={number}
                  >

                    <div className="pipeline-number">
                      {number}
                    </div>

                    <div>

                      <strong>
                        {title}
                      </strong>

                      <span>
                        {description}
                      </span>

                    </div>

                    <div className="pipeline-check">

                      {analyzing || result
                        ? "✓"
                        : "○"}

                    </div>

                  </div>

                )
              )}

            </div>

          </div>

        </section>


        {/* RESULTS */}

        {result && (

          <section className="results">

            <div className="results-heading">

              <div>

                <div className="eyebrow">
                  ANALYSIS COMPLETE
                </div>

                <h2>
                  Vulnerability Assessment
                </h2>

              </div>

              <span className="result-status red">
                {result.status}
              </span>

            </div>


            <div className="result-grid">


              {/* MAIN FINDING */}

              <div className="finding-card main-finding">

                <span className="label">
                  DETECTED VULNERABILITY
                </span>

                <h3>
                  {result.title}
                </h3>

                <div className="cwe">
                  {result.cwe}
                </div>

                <p>
                  Source-code patterns indicate
                  behavior associated with this
                  vulnerability class.
                </p>

              </div>


              {/* RISK */}

              <div className="metric-card">

                <span>
                  RISK SCORE
                </span>

                <strong>
                  {result.risk}%
                </strong>

                <div className="meter">

                  <i
                    style={{
                      width: `${result.risk}%`
                    }}
                  />

                </div>

                <small>
                  Neuro-Fuzzy risk estimate
                </small>

              </div>


              {/* CONFIDENCE */}

              <div className="metric-card">

                <span>
                  CONFIDENCE
                </span>

                <strong>
                  {result.confidence}%
                </strong>

                <div className="meter confidence">

                  <i
                    style={{
                      width:
                        `${result.confidence}%`
                    }}
                  />

                </div>

                <small>
                  Model confidence estimate
                </small>

              </div>


              {/* SECURITY TEST */}

              <div className="finding-card">

                <span className="label">
                  SELECTED SECURITY TEST
                </span>

                <h3>
                  {result.test}
                </h3>

                <p>
                  Generated or selected for
                  the detected vulnerability category.
                </p>

                <button className="secondary-btn">
                  VIEW TEST CASE
                </button>

              </div>


              {/* FEATURES */}

              <div className="finding-card feature-card">

                <span className="label">
                  KEY FEATURES
                </span>

                {result.features.map(
                  (feature) => (

                    <div
                      className="feature"
                      key={feature}
                    >

                      <span>
                        ✓
                      </span>

                      {feature}

                    </div>

                  )
                )}

              </div>

            </div>

          </section>

        )}


        {/* PHASE 2 */}

        <section className="next-phase">

          <div>

            <span className="eyebrow">
              NEXT
            </span>

            <h2>
              Phase 2 · Automated Security Patch Validation
            </h2>

            <p>
              Run the same security test against vulnerable
              and patched versions, compare behavior, and
              determine whether the patch actually fixes
              the vulnerability.
            </p>

          </div>

          <span className="locked">
            COMING NEXT
          </span>

        </section>

      </main>

    </div>
  );
}

export default App;