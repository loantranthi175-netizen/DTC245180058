# Sử dụng base image Node.js Alpine nhẹ và bảo mật
FROM node:20-alpine

# Thiết lập thư mục làm việc trong container
WORKDIR /usr/src/app

# Thiết lập môi trường sản xuất
ENV NODE_ENV=production

# Sao chép package.json và package-lock.json
COPY package*.json ./

# Cài đặt các thư viện sản xuất
RUN npm ci --omit=dev && npm cache clean --force

# Sao chép toàn bộ mã nguồn ứng dụng
COPY --chown=node:node . .

# Chuyển sang người dùng non-root 'node' để tăng cường bảo mật
USER node

# Mở cổng 3000
EXPOSE 3000

# Khởi chạy ứng dụng
CMD ["node", "server.js"]
