# 🚗 Gotcha : 딥러닝 기반 블랙박스 영상 속 불법주정차 실시간 탐지 및 자동 신고 클라우드 서비스

![Logo](./Logo.png)

## Skills

<div align="center"> 
  <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> 
  <img src="https://img.shields.io/badge/opencv-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white"> 
  <img src="https://img.shields.io/badge/yolo-149EF2?style=for-the-badge&logoColor=white"> 
  <img src="https://img.shields.io/badge/easyocr-3C2179?style=for-the-badge&logoColor=white">
  <img src="https://img.shields.io/badge/pytorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white"> 
  <br>
  <img src="https://img.shields.io/badge/amazons3-569A31?style=for-the-badge&logo=amazons3&logoColor=white"> 
  <img src="https://img.shields.io/badge/awslambda-FF9900?style=for-the-badge&logo=awslambda&logoColor=white"> 
  <img src="https://img.shields.io/badge/amazoncloudwatch-FF4F8B?style=for-the-badge&logo=amazoncloudwatch&logoColor=white"> 
</div>

## Main Process

1차: 배경 인식
- 불법주정차 금지구역임을 인지하고 어떤 유형에 해당하는지 판단

2차: 주정차 구분
- 인식된 객체를 분석하여 해당 객체의 정지 여부 판단

3차: 번호판 인식 및 메타데이터 추출
- 불법주정차로 판단된 경우, 해당 영상 이미지에서 차량 번호와 위치, 시간 등의 정보 추출
  
  (1) 번호판 인식
  
  (2) 이미지에서 메타데이터 추출
  
  (3) 신고 대상 필터링 후 로깅
  

## Developers

<div align="center">
  <table>
    <tr>
      <td align="center"><img src="https://avatars.githubusercontent.com/u/113416590?v=4" width="150" height="150"/><br/>sohyun park<br/><a href="https://github.com/sohvun">@sohvun</a></td>
      <td align="center"><img src="https://avatars.githubusercontent.com/u/98378283?v=4" width="150" height="150"/><br/>Yeonwoo Kim<br/><a href="https://github.com/yuonllna">@yuonllna</a></td>
      <td align="center"><img src="https://avatars.githubusercontent.com/u/144310416?v=4" width="150" height="150"/><br/>huisoo<br/><a href="https://github.com/huiesoo">@huiesoo</a></td>
    </tr>
  </table>
</div>

