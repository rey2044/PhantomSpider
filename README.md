<p align="center">
  <img src="assets/phantomspider_icon.png" width="150" alt="PhantomSpider Icon"/>
</p>

# 🕷️ PhantomSpider v2.0.0 – Stealth BFS Web Crawler

**PhantomSpider** is a **stealth-ready, high-performance Python web crawler** built on **Breadth-First Search (BFS)** for structured and systematic URL discovery.
Crafted for **penetration testers, bug bounty hunters, and digital forensics professionals**, it combines speed, scope control, and stealth features like **random user-agent rotation** to evade detection.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Cross--platform-lightgrey)

---

![image]([https://github.com/user-attachments/assets/5ab03ea0-abc5-4e98-abfa-702a0716e091)](https://github.com/rey2044/PhantomSpider/blob/main/assets/page.png)

---

## ✨ Features

* 🔍 **Breadth-First Search (BFS) crawling** for wide and systematic discovery
* 🎨 **Rich terminal UI** with color-coded tables and progress indicators
* 🌐 **Domain-restricted crawling** to keep exploration in-scope
* 🧠 **Parameter-based deduplication** (`--dedup-params`) for clean results
* ⚡ **Random User-Agent rotation** to bypass simple bot detections
* ⏳ Configurable **timeouts & delays** for crawl tuning
* 📂 **Export findings** to structured reports:

  * `urls_discovered.txt`
  * `parameters_found.txt`
  * `deduped_params.txt`

---

## ⚙️ Installation

```bash
git clone https://github.com/rey2044/PhantomSpider.git
```

```bash
cd PhantomSpider
```

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🚀 Usage

### 🔧 Command-line Options

```bash
python PhantomSpider.py -u <url> [options]
```

### 🔗 Examples

```bash
# Crawl a single target
python PhantomSpider.py -u https://example.com

# Crawl from a list with timeout & delay
python PhantomSpider.py -l urls.txt -t 1 --req-timeout 10

# Save crawl results
python PhantomSpider.py -u https://example.com -s

# Deduplicate query parameter patterns
python PhantomSpider.py -u https://example.com --dedup-params

# Full stealth mode (save + dedup + random user agents)
python PhantomSpider.py -u https://example.com -s --dedup-params --rua
```

---

## 📂 Output Files (saved in `results/`)

| File                   | Description                                |
| ---------------------- | ------------------------------------------ |
| `urls_discovered.txt`  | All discovered and visited URLs            |
| `parameters_found.txt` | URLs containing query parameters           |
| `deduped_params.txt`   | Unique entries per parameter key structure |

---

## 🧠 Workflow

1. Starts with a **seed URL** or a list of targets.
2. Traverses links using **BFS crawling**.
3. Restricts exploration to **in-scope domains only**.
4. Detects and **deduplicates parameterized URLs**.
5. Outputs results with a **color-coded, professional terminal display**.

---

## 📦 Requirements

* Python 3.8+

`requirements.txt`:

```text
requests
beautifulsoup4
rich
```

---

## 📄 License

Released under the **MIT License** – see [LICENSE](LICENSE).

---

## 👨‍💻 Author

**Laykumar Patel**
Cyber Security Researcher | Digital Forensics & VAPT Expert

📧 Email: [laykumarhp67428@gmail.com](mailto:laykumarhp67428@gmail.com)
📞 Contact: +91 9327112912
🔗 GitHub: [@rey2044](https://github.com/rey2044)

---

## 💬 Contributions & Issues

Feedback and contributions are welcome!
👉 Open an [Issue](https://github.com/rey2044/PhantomSpider/issues) or submit a [Pull Request](https://github.com/rey2044/PhantomSpider/pulls).

