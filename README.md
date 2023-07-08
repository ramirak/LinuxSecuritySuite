# Linux Security Suite (LSS)
## Securing your Linux machines has never been easier !

<p align="center">
<img src="Screenshots/lss.jpg" width="300">
</p>

## Features
- Choose between different policies, comes with pre-built policy for basic usage.
- Add, edit, or remove rules from your chosen policy and save them to disk.
- Apply them at any time by using the apply policy button.
- Mark any policy as current active policy.
- Use a blocklist file to block dozens of ip addresses before the main chains applies.
- Ability to use domain names instead of IP addresses.
- Show latest dropped packets logs
- Monitor active connections and running processes

## Notes
- Iptables must be installed on the system (comes preinstalled in most linux distros).
- In order to see log files you must configure syslog-ng if it is not already comes with your linux.
- ./lss.py

## Screenshots

<style>
div.gallery {
  border: 1px solid #ccc;
}

div.gallery:hover {
  border: 1px solid #777;
}

div.gallery img {
  width: 100%;
  height: auto;
}

div.desc {
  padding: 15px;
  text-align: center;
}

* {
  box-sizing: border-box;
}

.responsive {
  padding: 0 6px;
  float: left;
  width: 24.99999%;
}

@media only screen and (max-width: 700px) {
  .responsive {
    width: 49.99999%;
    margin: 6px 0;
  }
}

@media only screen and (max-width: 500px) {
  .responsive {
    width: 100%;
  }
}

.clearfix:after {
  content: "";
  display: table;
  clear: both;
}
</style>

<div class="responsive">
  <div class="gallery">
    <a target="_blank" href="Screenshots/1.png">
      <img src="Screenshots/1.png" width="800">
    </a>
    <div class="desc">Security Dashboard</div>
  </div>
</div>


<div class="responsive">
  <div class="gallery">
    <a target="_blank" href="Screenshots/2.png">
      <img src="Screenshots/2.png" width="800">
    </a>
    <div class="desc">Policy Editor</div>
  </div>
</div>

<div class="responsive">
  <div class="gallery">
    <a target="_blank" href="Screenshots/3.png">
      <img src="Screenshots/3.png" width="800">
    </a>
    <div class="desc">Firewall Rules</div>
  </div>
</div>

<div class="responsive">
  <div class="gallery">
    <a target="_blank" href="Screenshots/4.png">
      <img src="Screenshots/4.png" width="800">
    </a>
    <div class="desc">Active Connections</div>
  </div>
</div>





