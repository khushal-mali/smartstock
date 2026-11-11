import { IsNotEmpty, IsNumber, IsOptional, Min, IsInt } from 'class-validator';
import { Type } from 'class-transformer';

export class CreateProductDto {
  @IsNotEmpty({ message: 'SKU is required' })
  sku: string;

  @IsNotEmpty({ message: 'Product name is required' })
  name: string;

  @IsNumber({ maxDecimalPlaces: 2 }, { message: 'Price must be a valid number' })
  @Min(0, { message: 'Price cannot be negative' })
  @Type(() => Number)
  price: number;

  @IsOptional()
  @IsInt()
  @Min(0)
  @Type(() => Number)
  quantity?: number;

  @IsInt()
  @Min(0)
  @Type(() => Number)
  reorderLevel: number;

  @IsInt()
  @Type(() => Number)
  categoryId: number;

  @IsInt()
  @Type(() => Number)
  supplierId: number;
}

