import { Test, TestingModule } from '@nestjs/testing';
import { UnauthorizedException } from '@nestjs/common';
import * as bcrypt from 'bcrypt';
import { AuthService } from './auth.service';
import { PrismaService } from '../prisma/prisma.service';

jest.mock('@nestjs/jwt', () => ({
  JwtService: jest.fn().mockImplementation(() => ({
    sign: jest.fn().mockReturnValue('mock_jwt_token_xyz'),
  })),
}));

import { JwtService } from '@nestjs/jwt';

describe('AuthService (Unit Tests)', () => {
  let service: AuthService;
  let prisma: PrismaService;
  let jwt: JwtService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        AuthService,
        JwtService,
        {
          provide: PrismaService,
          useValue: {
            user: {
              findUnique: jest.fn(),
            },
          },
        },
      ],
    }).compile();

    service = module.get<AuthService>(AuthService);
    prisma = module.get<PrismaService>(PrismaService);
    jwt = module.get<JwtService>(JwtService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });

  it('should successfully authenticate user with valid credentials', async () => {
    const hash = await bcrypt.hash('secret123', 10);
    const mockUser = {
      id: 1,
      name: 'System Admin',
      email: 'admin@smartstock.com',
      passwordHash: hash,
      role: 'ADMIN',
    };

    jest.spyOn(prisma.user, 'findUnique').mockResolvedValue(mockUser as any);

    const result = await service.login({ email: 'admin@smartstock.com', password: 'secret123' });
    expect(result).toHaveProperty('accessToken', 'mock_jwt_token_xyz');
    expect(result.user.email).toBe('admin@smartstock.com');
    expect(result.user.role).toBe('ADMIN');
  });

  it('should throw UnauthorizedException if email does not exist', async () => {
    jest.spyOn(prisma.user, 'findUnique').mockResolvedValue(null);

    await expect(
      service.login({ email: 'unknown@smartstock.com', password: 'password123' }),
    ).rejects.toThrow(UnauthorizedException);
  });

  it('should throw UnauthorizedException if password hash does not match', async () => {
    const hash = await bcrypt.hash('correctPassword', 10);
    const mockUser = {
      id: 2,
      name: 'Test Staff',
      email: 'staff@smartstock.com',
      passwordHash: hash,
      role: 'STAFF',
    };

    jest.spyOn(prisma.user, 'findUnique').mockResolvedValue(mockUser as any);

    await expect(
      service.login({ email: 'staff@smartstock.com', password: 'wrongPassword' }),
    ).rejects.toThrow(UnauthorizedException);
  });
});
