import { NestFactory } from '@nestjs/core';
import { ValidationPipe } from '@nestjs/common';
import { AppModule } from './app.module';
import { INestApplication } from '@nestjs/common';

let cachedApp: INestApplication;

async function createApp(): Promise<INestApplication> {
  if (cachedApp) return cachedApp;

  const app = await NestFactory.create(AppModule, { logger: ['error', 'warn'] });

  const allowedOrigins = process.env.FRONTEND_URL
    ? process.env.FRONTEND_URL.split(',').map((o) => o.trim())
    : ['http://localhost:3000', 'http://127.0.0.1:3000'];

  app.enableCors({
    origin: allowedOrigins,
    credentials: true,
  });

  app.setGlobalPrefix('api');

  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,
      forbidNonWhitelisted: true,
      transform: true,
    }),
  );

  await app.init();
  cachedApp = app;
  return app;
}

// Vercel serverless handler
export default async function handler(req: any, res: any) {
  const app = await createApp();
  const server = app.getHttpAdapter().getInstance();
  server(req, res);
}

// Local development
async function bootstrap() {
  const app = await createApp();
  const port = process.env.PORT || 5000;
  await app.listen(port);
  console.log(`🚀 SmartStock API running on port ${port}`);
}

if (require.main === module) {
  bootstrap();
}
