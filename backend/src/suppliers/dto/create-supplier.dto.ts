import { IsEmail, IsNotEmpty, IsPhoneNumber, IsOptional } from 'class-validator';

export class CreateSupplierDto {
  @IsNotEmpty({ message: 'Supplier name is required' })
  name: string;

  @IsNotEmpty({ message: 'Phone number is required' })
  phone: string;

  @IsEmail({}, { message: 'Valid email is required' })
  email: string;
}

