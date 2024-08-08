<h1>Solana Mnemonic Bruteforce Tool</h1>

<p>This tool attempts to brute-force a Solana public key by iterating each word in a 24-word seed phrase, one position at a time, using a provided wordlist. It compares the generated public key to a list of known Solana public keys to find matches.</p>

<h2>Features</h2>

<ul>
  <li>Generates public/private keypairs from mnemonics.</li>
  <li>Validates Solana public keys.</li>
  <li>Supports multi-core processing for faster bruteforcing.</li>
  <li>Saves discovered mnemonics, private keys, and public keys to a file.</li>
</ul>

<h2>Installation</h2>

<p>To use this tool, you'll need Python and the following packages. Install them using <code>pip</code>:</p>

<p><code>pip install bip-utils solders</code></p>

<h2>Usage</h2>

<h3>Prepare Your Environment</h3>

<ol>
  <li><strong>Wordlist:</strong> Create a file named <code>words.txt</code> containing a list of possible words for the seed phrase (one word per line).</li>
  <li><strong>Public Keys:</strong> Create a file named <code>addresses.txt</code> containing the public keys to be matched (one public key per line).</li>
</ol>

<h3>Running the Tool</h3>

<h4>On Windows</h4>

<ol>
  <li>Open Command Prompt.</li>
  <li>Navigate to the directory containing your script.</li>
  <li>Run the script with:</li>
</ol>

<p><code>python solseedfarmer.py</code></p>

<h4>On Linux</h4>

<ol>
  <li>Open Terminal.</li>
  <li>Navigate to the directory containing your script.</li>
  <li>Run the script with:</li>
</ol>

<p><code>python3 solseedfarmer.py</code></p>

<h3>Input</h3>

<ul>
  <li><strong>Number of CPU Cores:</strong> Specify the number of CPU cores to use for parallel processing (enter <code>0</code> to use all available cores).</li>
  <li><strong>Seed Phrase:</strong> Enter your 24-word seed phrase with spaces between each word.</li>
</ul>

<h3>Output</h3>

<ul>
  <li>If a match is found, the mnemonic, private key, and public key will be saved to <code>discovery.txt</code>.</li>
  <li>All discovered public keys will be saved to <code>discovered_keys.txt</code>.</li>
</ul>

<h2>License</h2>

<p>This project is licensed under the MIT License. See the <code>LICENSE</code> file for details.</p>

<h2>Disclaimer</h2>

<p>Use this tool at your own risk. The author is not responsible for any misuse or illegal activities conducted with this tool.</p>
