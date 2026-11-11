import { PrismaClient, Role } from '@prisma/client';
import * as bcrypt from 'bcrypt';

const prisma = new PrismaClient();

async function main() {
  console.log('Clearing existing data...');
  await prisma.saleItem.deleteMany();
  await prisma.sale.deleteMany();
  await prisma.purchaseItem.deleteMany();
  await prisma.purchase.deleteMany();
  await prisma.product.deleteMany();
  await prisma.category.deleteMany();
  await prisma.supplier.deleteMany();
  await prisma.user.deleteMany();

  console.log('Seeding Users...');
  const adminPassword = await bcrypt.hash('admin123', 10);
  const staffPassword = await bcrypt.hash('staff123', 10);

  const admin = await prisma.user.create({
    data: {
      name: 'System Admin',
      email: 'admin@smartstock.com',
      passwordHash: adminPassword,
      role: Role.ADMIN,
    },
  });

  const staff = await prisma.user.create({
    data: {
      name: 'Inventory Staff',
      email: 'staff@smartstock.com',
      passwordHash: staffPassword,
      role: Role.STAFF,
    },
  });

  console.log('Seeding Categories...');
  const catElectronics = await prisma.category.create({ data: { name: 'Electronics' } });
  const catOffice = await prisma.category.create({ data: { name: 'Office Supplies' } });
  const catBeverages = await prisma.category.create({ data: { name: 'Beverages' } });

  console.log('Seeding Suppliers...');
  const supApex = await prisma.supplier.create({
    data: {
      name: 'Apex Wholesale Corp',
      phone: '+91 98765 43210',
      email: 'orders@apexwholesale.com',
    },
  });

  const supMetro = await prisma.supplier.create({
    data: {
      name: 'Metro Office Mart',
      phone: '+91 91234 56789',
      email: 'contact@metroofficemart.in',
    },
  });

  const supPrime = await prisma.supplier.create({
    data: {
      name: 'Prime Refreshments Ltd',
      phone: '+91 99887 76655',
      email: 'sales@primerefreshments.com',
    },
  });

  console.log('Seeding Products...');
  // Product 1: Normal stock
  const p1 = await prisma.product.create({
    data: {
      sku: 'ELEC-LOGI-M185',
      name: 'Logitech Wireless Mouse M185',
      price: 850.00,
      quantity: 35,
      reorderLevel: 10,
      categoryId: catElectronics.id,
      supplierId: supApex.id,
    },
  });

  // Product 2: Low stock! (quantity <= reorderLevel)
  const p2 = await prisma.product.create({
    data: {
      sku: 'ELEC-DELL-KB216',
      name: 'Dell Wired Keyboard KB216',
      price: 650.00,
      quantity: 4,
      reorderLevel: 8,
      categoryId: catElectronics.id,
      supplierId: supApex.id,
    },
  });

  // Product 3: Normal stock
  const p3 = await prisma.product.create({
    data: {
      sku: 'OFF-A4-PAPER-75G',
      name: 'JK Copier A4 Paper 75 GSM (500 Sheets)',
      price: 340.00,
      quantity: 50,
      reorderLevel: 15,
      categoryId: catOffice.id,
      supplierId: supMetro.id,
    },
  });

  // Product 4: Low stock! (quantity <= reorderLevel)
  const p4 = await prisma.product.create({
    data: {
      sku: 'OFF-STA-PIN-NO10',
      name: 'Kangaro Stapler No. 10',
      price: 95.00,
      quantity: 3,
      reorderLevel: 10,
      categoryId: catOffice.id,
      supplierId: supMetro.id,
    },
  });

  // Product 5: Healthy stock
  const p5 = await prisma.product.create({
    data: {
      sku: 'BEV-NES-COF-200G',
      name: 'Nescafe Classic Instant Coffee 200g',
      price: 450.00,
      quantity: 24,
      reorderLevel: 6,
      categoryId: catBeverages.id,
      supplierId: supPrime.id,
    },
  });

  console.log('Seeding initial Purchase...');
  await prisma.purchase.create({
    data: {
      supplierId: supApex.id,
      userId: admin.id,
      total: 35 * 700 + 4 * 500,
      items: {
        create: [
          { productId: p1.id, quantity: 35, costPrice: 700.00 },
          { productId: p2.id, quantity: 4, costPrice: 500.00 },
        ],
      },
    },
  });

  console.log('Seeding initial Sale...');
  await prisma.sale.create({
    data: {
      invoiceNo: 'INV-202611-0001',
      userId: staff.id,
      total: 850.00,
      items: {
        create: [
          { productId: p1.id, quantity: 1, price: 850.00 },
        ],
      },
    },
  });

  console.log('Seeding finished successfully!');
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });

